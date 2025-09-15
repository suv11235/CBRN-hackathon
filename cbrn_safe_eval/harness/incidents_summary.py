from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .incidents import INCIDENTS_FILE


def read_incidents(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    by_domain = Counter(r.get("domain") for r in rows)
    by_style = Counter(r.get("crescendo_style") for r in rows)
    by_turn = Counter(r.get("turn") for r in rows)
    tiers = [((r.get("trigger") or {}).get("severity_tier")) for r in rows]
    tiers_int = [int(t) for t in tiers if isinstance(t, int) or (isinstance(t, str) and t.isdigit())]
    sws = [((r.get("harm") or {}).get("sws_weight") or 0.0) for r in rows]
    out: Dict[str, Any] = {
        "incident_count": total,
        "by_domain": dict(by_domain),
        "by_crescendo_style": dict(by_style),
        "by_turn": dict(by_turn),
        "tiers": {
            "counts": dict(Counter(tiers_int)),
            "max": max(tiers_int) if tiers_int else None,
        },
        "sws": {
            "sum": float(sum(sws)),
            "mean": float(sum(sws) / len(sws)) if sws else 0.0,
        },
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate incidents summary JSON for slides")
    parser.add_argument("--path", type=str, default=str(INCIDENTS_FILE), help="incidents.jsonl path")
    parser.add_argument("--out", type=str, default=None, help="output JSON file (defaults to results/incidents_summary.json)")
    args = parser.parse_args()

    path = Path(args.path)
    rows = list(read_incidents(path))
    summary = summarize(rows)
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parents[2] / "results" / "incidents_summary.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote summary: {out_path}")


if __name__ == "__main__":
    main()


