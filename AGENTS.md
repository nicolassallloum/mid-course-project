# AGENTS.md - Task Tracker Repository Guardrails

## Stack and repository shape
- Backend: Python 3.11, FastAPI, Pydantic v2, and Uvicorn in `app/`.
- Frontend: one vanilla HTML/CSS/JavaScript client in `frontend/index.html`.
- Tests: pytest and FastAPI TestClient in `tests/`.
- Storage: in-memory only; no production database is part of this course project.
- Final submission branch: `final-project`.

## Read-first and docs-first rules
1. Read `README.md`, `docs/midcourse/`, and the relevant source files before proposing a change.
2. Preserve the existing FastAPI backend, vanilla-JavaScript frontend, API contract, and Kanban workflow.
3. Do not rewrite the project into React, Vite, Node, a database-backed app, or another architecture.
4. Only change `app/` or `frontend/` for a small verified bug fix, security correction, or documentation-supported correction. Record any such edit in `docs/final-ai-review.md`.

## Scope and safety rules
- Do not add authentication, comments, notifications, a production database, or unrelated UI features.
- Never paste or commit credentials, tokens, `.env` values, production logs, or real personal/customer data.
- Do not weaken CI with `continue-on-error`, `|| true`, skipped tests, fallback dependency installation, or vague Python versions.
- Review every diff and run the real commands before accepting AI-generated work.
- If a changed line or configuration choice cannot be explained, do not submit it.

## Canonical commands
### Local API
```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Local frontend
```bash
python -m http.server 5500 --directory frontend
```
Open `http://localhost:5500/index.html`.

### Tests
```bash
python -m pytest tests/ -v
```

### Docker
```bash
docker build -t ai-task-tracker:final .
docker run --rm -p 8000:8000 --name ai-task-tracker ai-task-tracker:final
curl http://localhost:8000/health
```
