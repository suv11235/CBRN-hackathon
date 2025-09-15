from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class JudgeResult:
    refusal: bool
    severity: str  # one of: safe, low, medium, high, unknown
    reasons: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "refusal": self.refusal,
            "severity": self.severity,
            "reasons": self.reasons,
            "scores": self.scores,
        }


