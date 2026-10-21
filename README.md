# Nimbus RAG Quality Harness

A small retrieval-augmented generation (RAG) system for a fictional company, built to practise testing AI systems. The system itself is simple; most of the work is in the test suite around it: retrieval metrics, generation checks, red-team tests, LLM-as-judge calibration, and an MCP server with contract tests.

## What it does

It answers employee questions about "Nimbus Logistics" (HR policies, IT guides) from 12 fictional markdown documents. The documents contain deliberate traps, such as an archived leave policy with outdated numbers and sections on similar topics.

## Architecture

1. **Chunking:** each document is split at its `##` headings. Each chunk keeps its source file and section name, and the document title is prefixed so chunks make sense on their own.
2. **Indexing:** chunks are embedded with `all-MiniLM-L6-v2` and stored in ChromaDB (cosine similarity), with a `current` / `archived` status in the metadata.
3. **Retrieval (two stages):** the bi-encoder fetches the top 10 current chunks, then a cross-encoder (`ms-marco-MiniLM-L-6-v2`) reranks them and keeps the top 3.
4. **Generation:** `llama3.1:8b` via Ollama, at temperature 0, with a grounded prompt: answer only from the context, otherwise reply with a fixed refusal sentence.
5. **API (FastAPI):** `/retrieve`, `/generate` and `/ask`, so retrieval and generation can be tested separately.
6. **MCP server:** exposes `search_docs` (calls `/retrieve`) and a mock `create_it_ticket` (writes to a local file) to MCP clients such as Claude Code.

No orchestration framework (such as LangChain) is used, so every stage stays visible and testable on its own.

## Test layers

| Layer | What it checks | Tool | Needs an LLM |
|---|---|---|---|
| Retrieval | Recall@3, Precision@3, MRR on a golden set, plus a CI quality gate | pytest | No |
| Retrieval (API) | Expected source file in the top 3; archived policy never returned | Java, REST Assured | No |
| Generation | Final answers contain the expected facts; unanswerable questions are refused | Java, REST Assured | Yes |
| Red-team | Prompt injection, prompt extraction, jailbreak, PII, sensitive data, off-topic use | pytest | Yes |
| Judge calibration | Whether an LLM judge can score known-good, hallucinated and half-wrong answers | DeepEval | Yes |
| MCP server | Tool contract, current policy returned (archived never), ticket writes exactly one record | pytest, MCP in-memory client | No |
| CI | Retrieval tests on every push and pull request | GitHub Actions | No |

Known failures are marked as strict expected failures, so a fix or a regression can't go unnoticed.

## Results

**Cross-encoder reranker** (6 answerable golden questions):

| Metric | Before | After |
|---|---|---|
| Recall@3 | 0.83 | 1.00 |
| Precision@3 | 0.28 | 0.33 (maximum possible) |
| MRR | 0.72 | 1.00 |

One question's correct chunk moved from rank 4 to 1, and another's from rank 3 to 1.

**LLM-as-judge calibration** (DeepEval Faithfulness; pass criteria set before running: good ≥ 0.8, hallucinated ≤ 0.2, half-wrong 0.3–0.7):

| Judge | Good | Hallucinated | Half-wrong |
|---|---|---|---|
| llama3.1:8b | 0.00 | 0.00 | 0.00 |
| qwen2.5:14b | 1.00 | 0.00 | 0.00 |

Neither judge passed. qwen2.5:14b still makes the right pass/fail decision at a 0.7 threshold, but isn't reliable for precise scores.

## Findings

- **A red-team test was passing without checking anything.** An assert inside a loop over an empty list meant three attack tests had no assertions. Fixed.
- **Layered tests locate failures.** After the reranker fixed retrieval for one question, its generation test failed. Reading the source chunk showed the expected answer was stricter than the document, so the test oracle was corrected rather than tuning the prompt.
- **Distance is not a refusal signal.** Best-match distances for answerable and unanswerable questions overlapped on this golden set, so refusal is left to the grounded prompt.
- **Prompt extraction still succeeds.** The model repeats its own instructions; a prompt alone can't prevent this.
- **The 8B model can't judge its own output.** It scored every answer 0, including the correct one.
- **Agents don't always use the tools you give them** (observed manually with Claude Code). With file access, the agent read the documents directly and bypassed `search_docs` and its archived-document filter. On the MCP path, the agent's own model writes the answer, so the RAG prompt's defences don't apply.

## Known limitations

- The golden set is small: 6 answerable questions and 1 unanswerable.
- Chunk IDs are position-based, so adding a section shifts IDs and breaks golden labels.
- The generation tests call `/ask`, so they can't isolate generation from retrieval.
- Some red-team refusals may happen because the information isn't in the corpus, not because the model recognised a sensitive request.
- Automated agent tests (`evals/test_agent.py`) are skipped: Claude Code's headless mode did not apply MCP tool permissions in this setup.
- CI runs the retrieval tests only; LLM-dependent tests run locally.

## Running it

**Requirements:** Python 3.14, [Ollama](https://ollama.com) with `llama3.1:8b`, and Java 21 with Maven for the Java tests.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1:8b
python app/index.py
uvicorn api:app --app-dir app
```

The API runs at `http://127.0.0.1:8000` (Swagger UI at `/docs`). With the API running, in a second terminal:

```
pytest evals -v -s
cd tests && mvn test
```

**Judge calibration** (needs about 9 GB of free RAM):

```
ollama pull qwen2.5:14b
python evals/judge_check.py qwen2.5:14b
```

**Connect the MCP server to Claude Code:**

```
claude mcp add nimbus -- /path/to/project/.venv/bin/python /path/to/project/app/mcp_server.py
```

## Project structure

```
app/        chunking, indexing, search, answer generation, FastAPI app, MCP server
corpus/     12 fictional Nimbus Logistics documents (handbook/, it/)
golden/     golden question set (golden.json)
evals/      pytest: retrieval metrics, red-team, judge calibration, MCP server and agent tests
tests/      Java: Maven, JUnit 5, REST Assured API tests
.github/    CI workflow (retrieval quality gate)
```

## Tools

Python, FastAPI, ChromaDB, sentence-transformers, Ollama, DeepEval, pytest, MCP Python SDK, Java, JUnit 5, REST Assured, GitHub Actions. Developed with Claude Code as an AI pair programmer.