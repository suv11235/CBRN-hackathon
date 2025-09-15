# CBRN-SAFE-Eval Prototype Plan

## Goal

Build a prototype evaluation framework to test LLMs/models for CBRN-misuse risk failure modes, including Crescendo (multi-turn escalation), many-shot / example injection, persona/role attacks, prompt injection, etc. Deliver a working harness + small prompt bank + judge + dashboard + scorecard in 2 days.

---

## Timeline & Tasks

| Time | Tasks |
|---|---|
| **Before hack-sprint / “Day 0”** | 🎯 Preparations: set up repo scaffold; collect or write safe prompt bank; gather any needed datasets; decide which model(s) to test (local open model + cloud API) |
| **Day 1 Morning** | • Implement core harness: code to run a model for a prompt, record output <br> • Implement basic prompt transforms: Crescendo escalation, many-shot, persona, paraphrase <br> • Write ~20 base prompts (non-actionable, safe) covering biology, chemistry, radiology, nuclear, etc. |
| **Day 1 Afternoon** | • Build auto-judge module: refusal detection + severity classification (High/Med/Low) via lightweight methods (keyword + simple LLM judge + manual spot checks) <br> • Run initial evaluation on model(s) with base + transformed prompts; collect results <br> • Save logs & outputs (with safe redaction, if necessary) |
| **Day 1 Evening** | • Create basic metrics: success rates per threat type, Crescendo turn failure point, consistency across persona transforms <br> • Build minimal dashboard (e.g. Streamlit / Flask) to visualize results (tables, plots) |
| **Day 2 Morning** | • Add mitigation experiments: e.g. system prompt guardrail, output filtering, stricter judge thresholds <br> • Re-run evaluation with mitigations; compare metrics |
| **Day 2 Afternoon** | • Polish prompt bank and transformations; ensure no unsafe or disallowed content <br> • Build scorecard generator: summary PDF/Markdown with metrics, severity, recommended mitigations, policy checklist <br> • Finalize dashboard and repo instructions <br> • Prepare demo: slides/screenshots, live run of Crescendo sequence, etc. |

---

## To-Do List

- [ ] Initialize repo scaffolding with directories & placeholder files  
- [ ] Collect / write safe base prompts (~20) with diversity across CBRN subdomains  
- [ ] Define prompt transforms (Crescendo, many-shot, persona, paraphrase) and write scripts to apply them  
- [ ] Integrate 1-2 models: ideally one open source (locally runnable) + one via API (if permissions/cost allow)  
- [ ] Create judge module (thresholds for refusal vs non-refusal; severity labeling)  
- [ ] Design & compute metrics (attack success, severity, consistency, Crescendo turn)  
- [ ] Create dashboard to present results (plots, tables), maybe using Streamlit  
- [ ] Implement mitigation options and compare results pre/post mitigation  
- [ ] Prepare scorecard / summary report, with policy/guidance suggestions  
- [ ] Demo plan: pick example prompts & transforms to show how failure happens; show mitigations  

---

## Risks & Mitigations

- If model gives disallowed content accidentally → use safe prompts only; have judge that rejects; human spot checking; avoid asking for detailed protocols.  
- If API costs/time are high → keep sample size small; focus on quality of prompts rather than quantity.  
- If time runs short → prioritize core harness + Crescendo transform + judge + one model + initial dashboard. Mitigations & polish can come after.

---

## Deliverables

1. **GitHub repo** with code: harness, transforms, judge, prompt bank  
2. **Prompt bank** (base + transforms) with clear documentation that all are safe / non-actionable  
3. **Evaluation run** on at least one model showing results for attack types including Crescendo  
4. **Dashboard** showing metrics / plots / tables  
5. **Scorecard / summary report** + recommended mitigations + policy checklist  
6. **Demo materials**: slides & maybe live or recorded run of one Crescendo sequence  

---

## Success Criteria (for hackathon)

- Clearly demonstrates that the tool exposes failure modes (e.g. Crescendo) in at least one model  
- Metrics are easy to interpret, dashboard is usable, repo is clean and runnable  
- Mitigation experiments show measurable improvement (even if partial)  
- Presentation emphasizes safety, info-hazards, ethical design  

