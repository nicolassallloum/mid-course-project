# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-06
- Local API run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `/health` result: HTTP 200 with `{"status":"ok"}`.
- Frontend run command: `python -m http.server 5500 --directory frontend`.
- Frontend check: Chromium loaded the three-column Kanban board; a task was created through the modal, displayed in To Do, edited to In Progress, and the UI refreshed from the FastAPI backend.
- Test command: `python -m pytest tests/ -v`
- Test result: `31 passed`.
- Scope check: no new product feature was added to `app/` or `frontend/`; the final work adds only release configuration and evidence documentation.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Trigger: pushes to `main`, `mid-course-project`, and `final-project`; pull requests to `main` and `final-project`.
- Python version: exact `3.11`.
- Dependency command: `python -m pip install -r requirements.txt`.
- Test command used by CI: `python -m pytest tests/ -v`.
- Shortcut check: no `continue-on-error`, no `|| true`, no skipped pytest command, and no fallback dependency installation.
- Latest green run link or note: **Pending first push to the public GitHub repository. Replace this note with the real green Actions run link before LMS submission.**

## Docker evidence

- Dockerfile runtime: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Build command: `docker build -t ai-task-tracker:final .`
- Run command: `docker run --rm -p 8000:8000 --name ai-task-tracker ai-task-tracker:final`
- `/health` check command: `curl -i http://localhost:8000/health`
- Non-root check: the image creates and runs as `appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, `.git`, virtual environments, caches, and logs.
- Local Docker result: **Pending because Docker is not available in the preparation environment. Run the commands above and replace this note with the real build/run/HTTP 200 result before LMS submission.**

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made |
|---|---|---|---|
| The project is a FastAPI backend with a vanilla-JavaScript frontend | `app/main.py`, `frontend/index.html`, and local runtime check | Verified | Removed the React/Vite `npm run dev` instructions from the invalid final snapshot |
| `GET /health` returns HTTP 200 and `{"status":"ok"}` | Real Uvicorn process and HTTP request | Verified | README now states the actual response and port 8000 |
| The full test suite contains 31 passing tests | `python -m pytest tests/ -v` | Verified | README and this evidence file record the actual count |
| Docker should launch the API with `python -m app.main` on port 3000 | Actual `app/main.py` and Uvicorn architecture | False | Dockerfile corrected to run Uvicorn on port 8000 |
