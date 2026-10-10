# RAG Testing Project

## Who I am
Hassan, QA Automation Engineer, about 4 years (Java, Selenium, Serenity, REST Assured, JUnit, SQL, Git). Working knowledge of Python. New to AI/LLM concepts. I don't code daily, so I forget syntax. I'm preparing for an AI QA Engineer interview. The job description is in `docs/JD.md`; read it when mapping work to the JD.

## Honesty rule (most important)
Help me learn. Never help me fake experience. Everything I claim in the interview must be something I built, ran, and understand. Never call a step done unless it was run and I saw the output.

## How to work with me
- Simple words. One idea at a time. Short messages. Too many new terms at once overwhelm me.
- Explain the "why" in plain language first, then the code.
- Before editing any file: tell me which files and what will change, then wait for my OK.
- Work in small steps. After each change, give the exact command to run and the expected result.
- Explain code section by section (not line by line), including how the pieces connect.
- At the end of each step: interview Q&A. Explain the concept generally (as in an interview), then how I used it here. Focus on AI/testing concepts, not Python setup trivia. Map to the JD.
- Shell commands: one per code block, no inline comments (zsh treats # and ; oddly when pasted).
- Keep scope tight: one finished project. Remind me if I try to add scope.
- At the end of each step, propose updates to docs/PROJECT_STATUS.md and show me the change before saving.

## Environment
- MacBook M5, 16 GB RAM, macOS, zsh. IntelliJ (no Python plugin; Python runs from terminal). GitHub Desktop.
- Project path has a typo and a space: "/Users/Shared/D folder/rag-testing-projec"
- Python 3.14 venv at .venv. Every new terminal: source .venv/bin/activate
- Ollama runs as a brew service, model llama3.1:8b, API at localhost:11434.

## Commands
- Start API (port 8000, Swagger at /docs): uvicorn api:app --app-dir app
- pytest evals (from project root, API running): pytest evals -v -s
- Java tests (API running): cd tests, then mvn test
- Label helper: python evals/label_helper.py

## Structure
- corpus/: 12 fictional "Nimbus Logistics" docs (handbook/, it/) with deliberate traps
- app/: chunking.py, index.py, search.py, answer.py, api.py (FastAPI: /retrieve, /generate, /ask)
- golden/: golden_draft.md and golden.json (GD-01 to GD-07)
- tests/: Java suite (Maven, JUnit 5, REST Assured): API and contract tests
- evals/: pytest suite: retrieval metrics, and all new eval work
- Language split: Java = API/contract tests. All new eval work = pytest.

## Current status
@docs/PROJECT_STATUS.md