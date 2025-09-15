CBRN-SAFE-Eval

Quick start

1) Create a virtual environment
   python3 -m venv .venv
   source .venv/bin/activate

2) Install dependencies
   pip install -r requirements.txt

3) Configure environment
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY

4) Run a dry run (no API calls yet)
   python -m cbrn_safe_eval.harness.runner --list-prompts

Structure

- prompts/: base prompts and templates (functional)
- transforms/: prompt transformation scripts (functional)
- harness/: runner, model interface, prompt manager (functional)
- judge/: refusal detection and severity classifier (functional)
- mitigations/: optional mitigations (system prompt guard, filters) (functional)
- dashboard/: basic visualization app (not functional)
- results/: logs, raw outputs, metrics (functional)
- report/: scorecard and slides (not functional)

Safety note

This project evaluates models using only safe, non-actionable prompts related to CBRN. Do not add or use content that could facilitate harm.
