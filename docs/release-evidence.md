# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-06
- Local API run command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8002`
- `/health` result: HTTP 200 with `{"status":"ok"}`.
- Frontend run command: `python -m http.server 5500 --directory frontend`.
- Frontend check: The three-column Kanban board loaded and the create/edit flow remained available.
- Test command: `python -m pytest tests/ -v`
- Test result: `31 passed, 3 warnings in 0.27s`.
- Scope check: no new product feature was added to `app/` or `frontend/`; the final work adds only release configuration and evidence documentation.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Trigger: pushes and pull requests involving `main`, `mid-course-project`, and `final-project`.
- Python version: exact `3.11`.
- Dependency command: `python -m pip install -r requirements.txt`.
- Test command used by CI: `python -m pytest tests/ -v`.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Latest green run note: Task Tracker CI completed successfully on the `final-project` branch on 2026-08-06.

## Docker evidence

- Dockerfile runtime: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Build command: `docker build -t task-tracker-final .`
- Build result: Successful; Docker image `task-tracker-final` was created.
- Run command: `docker run -d --rm --name task-tracker-final-check -p 8010:8000 task-tracker-final`
- `/health` check: `curl -i http://127.0.0.1:8010/health`
- `/health` result: HTTP 200 with `{"status":"ok"}`.
- Non-root check: The image runs as `appuser`.
- No-baked-secrets check: `.dockerignore` excludes environment files, Git metadata, virtual environments, caches, and logs.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made |
|---|---|---|---|
| The project is a FastAPI backend with a vanilla-JavaScript frontend | `app/main.py`, `frontend/index.html`, and local runtime check | Verified | Removed the React/Vite `npm run dev` instructions from the invalid final snapshot |
| `GET /health` returns HTTP 200 and `{"status":"ok"}` | Real Uvicorn process and HTTP request | Verified | README now states the actual response and port 8000 |
| The full test suite contains 31 passing tests | `python -m pytest tests/ -v` | Verified | README and this evidence file record the actual count |
| Docker should launch the API with `python -m app.main` on port 3000 | Actual `app/main.py` and Uvicorn architecture | False | Dockerfile corrected to run Uvicorn on port 8000 |
