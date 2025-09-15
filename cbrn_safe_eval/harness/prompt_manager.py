import os
from pathlib import Path
from typing import List, Dict


class PromptManager:
    """
    Loads base prompts and templates from the prompts directory.
    Only safe, non-actionable content should be included.
    """

    def __init__(self, prompts_root: str | os.PathLike | None = None) -> None:
        self.prompts_root = Path(prompts_root or Path(__file__).resolve().parents[1] / "prompts")

    def list_base_prompts(self) -> List[Path]:
        base_dir = self.prompts_root / "base_prompts"
        if not base_dir.exists():
            return []
        return sorted([p for p in base_dir.iterdir() if p.is_file() and p.suffix in {".txt", ".md"}])

    def load_prompt(self, path: str | os.PathLike) -> str:
        p = Path(path)
        return p.read_text(encoding="utf-8")

    def load_all_base_prompts(self) -> Dict[str, str]:
        prompts: Dict[str, str] = {}
        for p in self.list_base_prompts():
            prompts[p.name] = self.load_prompt(p)
        return prompts


