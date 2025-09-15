from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Iterable

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


def main() -> None:
    parser = argparse.ArgumentParser(description="List and filter incidents")
    parser.add_argument("--path", type=str, default=str(INCIDENTS_FILE), help="incidents.jsonl path")
    parser.add_argument("--domain", type=str, default=None, help="filter by domain")
    parser.add_argument("--min-tier", type=int, default=None, help="filter by minimum severity tier")
    parser.add_argument("--style", type=str, default=None, help="filter by crescendo style")
    args = parser.parse_args()

    path = Path(args.path)
    rows = list(read_incidents(path))
    out = []
    for r in rows:
        if args.domain and r.get("domain") != args.domain:
            continue
        tier = ((r.get("trigger") or {}).get("severity_tier"))
        if args.min_tier is not None:
            try:
                if int(tier) < int(args.min_tier):
                    continue
            except Exception:
                continue
        if args.style and r.get("crescendo_style") != args.style:
            continue
        out.append(r)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


