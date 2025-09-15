from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


def list_latest_redactions(raw_dir: str, window_minutes: int = 30) -> list[dict]:
    root = Path(raw_dir)
    files = sorted(root.glob("*.json"))
    entries: list[tuple[datetime, Path]] = []
    for f in files:
        m = re.match(r"(\d{8}T\d{6}Z)__", f.name)
        if not m:
            continue
        ts = datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        entries.append((ts, f))
    if not entries:
        return []
    entries.sort()
    latest_ts = entries[-1][0]
    cutoff = latest_ts - timedelta(minutes=window_minutes)
    latest_files = [f for ts, f in entries if ts >= cutoff]

    results: list[dict] = []
    for f in latest_files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("mode") == "crescendo":
            for item in data.get("sequence", []):
                rubric = ((item.get("judge") or {}).get("rubric") or {})
                if rubric.get("redact"):
                    results.append({
                        "file": f.name,
                        "prompt_name": data.get("prompt_name"),
                        "crescendo_style": data.get("crescendo_style"),
                        "turn": item.get("turn"),
                        "user": (item.get("user") or "").strip(),
                        "indicators": rubric.get("indicators", []),
                    })
        else:
            judge = data.get("judge") or {}
            rubric = judge.get("rubric") or {}
            if rubric.get("redact"):
                results.append({
                    "file": f.name,
                    "prompt_name": data.get("prompt_name"),
                    "crescendo_style": None,
                    "turn": 1,
                    "user": (data.get("prompt_text") or "").strip(),
                    "indicators": rubric.get("indicators", []),
                })
    return results


if __name__ == "__main__":
    raw_dir = str(Path(__file__).resolve().parents[2] / "results" / "raw_outputs")
    rows = list_latest_redactions(raw_dir)
    if not rows:
        print("No redactions in the latest batch window.")
    else:
        for r in rows:
            user = r["user"].replace("\n", " ")
            if len(user) > 180:
                user = user[:177] + "..."
            print(
                f"file={r['file']} prompt={r['prompt_name']} style={r['crescendo_style']} "
                f"turn={r['turn']} indicators={r['indicators']}\nuser: {user}\n"
            )


