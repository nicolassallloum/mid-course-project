# AI-Assisted Task Tracker

This is the original FastAPI and vanilla-JavaScript Task Tracker used for the mid-course project, now extended only with final-course release-readiness and AI-ownership evidence.

The application keeps the mid-course features and architecture intact:

1. Due dates and an overdue filter.
2. Search with combined status, priority, assignee, and overdue filters.
3. The original three-column Kanban board and validated status-transition rules.

## Repository branches

- `main`: reconstructed baseline of the submitted mid-course Task Tracker.
- `mid-course-project`: points to the same preserved mid-course baseline.
- `final-project`: adds CI, Docker, repository guardrails, and final evidence documents without replacing the application.

> The uploaded ZIP files did not contain their original `.git` histories. The branch structure in this package was reconstructed from the actual mid-course source snapshot.

## Existing behavior preserved

- FastAPI backend in `app/`.
- Vanilla HTML/CSS/JavaScript frontend in `frontend/index.html`.
- In-memory task storage.
- `GET /health` returning `{"status":"ok"}`.
- Create, list, read, update, and delete task endpoints.
- Strict Pydantic models and extra-field rejection.
- Allowed transitions: `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`.
- Due dates, computed overdue status, search, and combined filters.
- Native drag-and-drop with server persistence and rollback on rejected transitions.

## Project structure

```text
.github/workflows/ci.yml
Dockerfile
.dockerignore
AGENTS.md
README.md
app/
frontend/
tests/
docs/
  midcourse/
  release-evidence.md
  final-ai-review.md
  ai-playbook.md
```

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker remains within the intended course scope.
- CI installs the declared dependencies and runs the full pytest suite on pushes and pull requests.
- The Docker image starts the actual FastAPI application on port 8000 and defines a `/health` health check.
- AI review, security review, correction decisions, and personal ownership rules are recorded in `docs/`.

### How to run locally

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies and start the API:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Verify:

- Health: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`

In a second terminal, serve the frontend:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500/index.html`.

### How to run tests

```bash
python -m pytest tests/ -v
```

The reconstructed final branch was verified with all 31 tests passing.

### How to run with Docker

```bash
docker build -t ai-task-tracker:final .
docker run --rm -p 8000:8000 --name ai-task-tracker ai-task-tracker:final
```

In another terminal:

```bash
curl -i http://localhost:8000/health
```

Expected response body:

```json
{"status":"ok"}
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`
- Existing mid-course evidence remains in `docs/midcourse/`.

### AI assistance summary

AI helped compare the two uploaded repository snapshots, identify that the React/Vite application was not the original course project, and draft the release configuration and evidence documents. I verified the actual FastAPI application by reviewing the diff, running the full pytest suite, starting the API, checking `/health`, and testing the frontend workflow in a browser. I rejected the suggestion implied by the separate generated repository to replace the original application with a React/Vite project.
