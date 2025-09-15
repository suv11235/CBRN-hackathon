from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


try:
    # Lazy import placeholder; we import inside methods to allow non-API smoke checks
    from openai import OpenAI
    from openai import APIError, RateLimitError
except Exception:  # pragma: no cover - only for environments without openai installed
    OpenAI = None  # type: ignore
    class APIError(Exception):
        pass
    class RateLimitError(APIError):
        pass


@dataclass
class OpenAIConfig:
    model: str
    temperature: float = 0.2
    max_tokens: int = 512

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        load_dotenv()  # load from .env if present
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "512"))
        return cls(model=model, temperature=temperature, max_tokens=max_tokens)


class OpenAIClient:
    """
    Thin wrapper around OpenAI Chat Completions for uniform interface.
    """

    def __init__(self, config: Optional[OpenAIConfig] = None) -> None:
        self.config = config or OpenAIConfig.from_env()
        # Do not initialize the client until needed to allow config checks without API key
        self._client: Optional[OpenAI] = None  # type: ignore

    def _ensure_client(self) -> None:
        if self._client is None:
            if OpenAI is None:
                raise RuntimeError("openai package is not installed. Run: pip install -r requirements.txt")
            load_dotenv()
            if not os.getenv("OPENAI_API_KEY"):
                raise RuntimeError("OPENAI_API_KEY is not set. Create .env and export the key.")
            self._client = OpenAI()

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((RateLimitError, APIError)),
    )
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """
        Call OpenAI chat completions and return a dict with text and token usage.
        messages: list of {role: "system"|"user"|"assistant", content: str}
        """
        self._ensure_client()
        assert self._client is not None
        params = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs,
        }
        resp = self._client.chat.completions.create(messages=messages, **params)
        text = resp.choices[0].message.content if resp.choices else ""
        usage = getattr(resp, "usage", None)
        return {
            "text": text,
            "usage": {
                "prompt_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
                "completion_tokens": getattr(usage, "completion_tokens", None) if usage else None,
                "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
            },
            "raw": resp.model_dump() if hasattr(resp, "model_dump") else resp,  # for debugging
        }

    def generate_from_text(self, user_text: str, system_text: str | None = None, **kwargs: Any) -> Dict[str, Any]:
        messages: List[Dict[str, str]] = []
        if system_text:
            messages.append({"role": "system", "content": system_text})
        messages.append({"role": "user", "content": user_text})
        return self.generate(messages, **kwargs)


