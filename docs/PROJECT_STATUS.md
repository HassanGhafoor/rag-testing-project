# Project Status

## Built
- RAG pipeline: chunk on "## " headings (12 docs -> 111 chunks, ID like handbook/benefits.md::2), MiniLM embeddings in Chroma (cosine, metadata status current/archived), retrieve top 3 with where status=current, Ollama llama3.1:8b answers only from context at temperature 0, else "I don't know based on the company documents."
- Golden set (golden.json): fields id, question, expectedSources, expectedChunkIds, answerContains, answerable. All labels verified with grep.
    - GD-01 health insurance self = 800,000, benefits.md::2 (table; family 500,000 is the distractor)
    - GD-02 annual leave = 22, leave-policy.md::2 (archived doc says 18)
    - GD-03 premium economy = flights over 8 hours, expenses-and-travel.md::4
    - GD-04 6-hour flight = No, expenses-and-travel.md::4
    - GD-05 OS updates within 7 days, laptop-policy.md::4 (distractors: password "7 days", software "10 working days")
    - GD-06 VPN blocked = hotspot, then IT ticket, vpn-setup.md::7 Troubleshooting (verified: line 74 is inside the section)
    - GD-07 parking = unanswerable
- Java suite: 8 tests passing (smoke, file-level retrieval Recall@3 6/6, archived never retrieved). GoldenCase needs @JsonIgnoreProperties(ignoreUnknown = true).
- pytest retrieval evals (evals/test_retrieval.py): first run 7 passed, 1 failed. Recall@3 = 0.83, Precision@3 = 0.28, MRR = 0.72 (verified by hand).
- DeepEval generation evals: Hassan says implemented. NOT yet reviewed. Read the evals/ folder to confirm what exists before relying on it.

## Findings (real interview stories)
- Archived policy ranked 1st -> fixed with a metadata status filter; archived doc kept as a regression trap; proved the test fails when the filter is removed.
- GD-02 expected 18 but system said 22 -> the TEST was wrong (18 is archived). Now every expected value is verified with grep.
- "7 days" in two unrelated docs -> a correct answer can hide a retrieval failure, so retrieval is tested separately.
- Parking correctly refused (grounding works).
- Non-determinism seen: "The answer is 4." vs "2 + 2 = 4".
- Chunking checks: table intact, 111 in = 111 stored, weak chunks, MiniLM ~256-token truncation risk.
- GD-06: answer chunk ranks 4th, a near-tie (0.591) with remote-work::7. The Java file-level check hid this; the chunk-level check caught it.
- Aggregate gate passed (0.83 >= 0.8) while GD-06 failed: averages hide individual failures, so keep per-case tests and the aggregate gate.
- Threshold 0.45 test passed but only checked one side. Answerable best distances run 0.34 to 0.58, and unanswerable parking is 0.461, in the middle. Distances are not calibrated, so no fixed threshold works. Distance = soft signal; the LLM's grounded refusal is the real safety layer.
- - DeepEval faithfulness with local llama3.1:8b judge: scored a correct answer 0.0. Verbose logs showed truths and claims extracted correctly but the final verdict wrong. Judge validation set (good / hallucinated / half-wrong) scored 0.0 on all three, so the judge failed validation and is not used for gating. Deferred: stronger judge.
- - Red-team: 6 attacks. Injection (PWNED) worked at first. Prompt hardening (tags, "user text is data" rule, sandwich reminder) fixed injection and jailbreak. First fix didn't reach the API (duplicated prompt in api.py), refactored to one build_prompt. Prompt extraction still leaks instructions: recorded as xfail. Caught a false pass (leaked text contained the refusal phrase). No over-refusal on normal questions.
- Java GenerationTest: answerContains checks with whole-word matching over all 7 golden cases. GD-06 fails because retrieval misses the chunk and the LLM correctly refuses: a downstream failure, recorded as a known failure.

## Plan
Step 1 (IN PROGRESS): finish retrieval evals
- A. k=5 experiment (predicted: Recall 1.00, MRR 0.76, Precision 0.20), record the numbers, revert to K=3
- B. Mark GD-06 xfail(strict=True) with a written reason (KNOWN_FAILURES dict + pytest.param)
- C. Replace the threshold test with a both-sides test that prints the distance table, xfail(strict=True) as a documented finding
- Expected after: 6 passed, 2 xfailed
  Step 2: Review the DeepEval work (faithfulness, answer relevancy, contextual precision/recall, one GEval rubric, local Ollama judge, human-review file for low scores). Be honest that an 8B judge is weak and noisy.
  Step 3: Red-team set (prompt injection, jailbreak, PII leakage, refusal), deterministic pass/fail.
  Step 4: GitHub Actions quality gate, retrieval metrics only, in a Docker container, with pinned requirements. Generation evals stay local (explain why).
  Step 5: Agent test scenario design (tool-call correctness, trajectory). Build a tiny agent only if time allows.
  Step 6: README with results, test strategy, interview talking points.
  CUT: Jenkins, MCP, promptfoo, Allure, load testing, Azure.

## Next action
Step 1, move A.