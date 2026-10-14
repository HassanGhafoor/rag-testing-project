## Plan (learning phase, started Oct 2026)
Goal: understand everything properly, not rush. One phase at a time; finish before adding scope.

Phase 1 (CURRENT): Own what I built
- Walk through each file: chunking.py, index.py, search.py, answer.py, api.py, retrieval_metrics.py, test_retrieval.py, test_redteam.py, Java tests, CI workflow
- For each: predict what it does, run it, explain it in my own words
- Break things on purpose (chunking, metadata filter, k, prompt), predict what fails, check
- Write the README myself in my own words

Phase 2: Finish evaluation properly
- Find a judge that passes evals/judge_check.py (good / hallucinated / half-wrong)
- Add a GEval rubric metric and a human-review file for low scores
- Run the same golden set through RAGAS and DeepEval, compare results

Phase 3: Fix GD-06 with a reranker, then hybrid search; measure MRR before/after

Phase 4: MCP + agents
- Build an MCP server for Nimbus: search_docs (RAG), get_leave_balance (mock), create_it_ticket (mock)
- Connect it to Claude Code or a small agent
- Write real tool-call and trajectory tests

Phase 5: Observability with Langfuse in Docker, latency and token cost

Knowledge track (alongside): read DeepEval, RAGAS, promptfoo, garak repos (README, examples, one metric's source code); one AI concept a day, explained out loud in 2 minutes

## Interview gaps to cover
- Questions about eval-framework repos
- Generic AI concept questions
- (add the specific questions I remember here)

## Next action
Phase 1, file 1: app/chunking.py