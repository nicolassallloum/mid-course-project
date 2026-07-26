# AI-Assisted Task Tracker — Mid-Course Feature Extension Sprint

This repository extends the Modules 1–3 FastAPI Task Tracker with two scoped, end-to-end features:

1. **Due dates + overdue filter**
2. **Search + combined filters**

The project preserves the original Module 2 backend rules and Module 3 Kanban workflow while adding visible frontend controls, backend validation/filtering, focused pytest coverage, Break Test evidence, and the required project documentation.

## Submission branch

The submitted branch must be named exactly:

```bash
git checkout -b mid-course-project
```

After extracting this project, initialize Git if needed, create that branch, commit the files, and push the branch to a **public** repository.

## Features

### Due dates + overdue filter

- Optional `due_date` accepted by create and update operations.
- ISO date validation through Pydantic.
- Computed `is_overdue` value returned by the API.
- A task is overdue when its due date is before today and its status is not `Done`.
- `GET /tasks?overdue=true` returns overdue tasks only.
- The create/edit modal includes a due-date field.
- Cards display the due date and an **Overdue** pill when applicable.

### Search + combined filters

- `GET /tasks?q=...` searches title and description case-insensitively.
- Search combines with `status`, `priority`, `assignee`, and `overdue` filters.
- No matches return HTTP 200 with `[]`.
- Invalid enum filters return HTTP 422.
- The frontend provides search, status, priority, overdue, and clear-filter controls.
- All three Kanban columns remain visible when a filter returns no cards for a column.

## Existing behavior preserved

- `/health` endpoint.
- Strict Pydantic v2 models and extra-field rejection.
- In-memory storage.
- Five CRUD endpoints.
- Status-transition rules:
  - `ToDo -> InProgress`
  - `InProgress -> Done`
  - `Done -> InProgress`
- Invalid and same-status transitions return 422.
- Loading, empty, ready, and error UI states.
- Native drag-and-drop with PATCH persistence and rollback on rejection.
- Create/edit modal with client title trimming and server error handling.

## Project structure

```text
app/
  main.py
  models.py
  storage.py
  business_rules.py
frontend/
  index.html
tests/
  conftest.py
  verify_a.py
  test_tasks.py
docs/midcourse/
  user-stories.md
  mini-adr.md
  prompt-log.md
  verification.md
  reflection.md
```

## Run the backend

### 1. Create a virtual environment

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

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Verify:

- Health: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`

## Open the frontend

In a second terminal:

```bash
python -m http.server 5500 --directory frontend
```

Open:

```text
http://localhost:5500/index.html
```

The backend CORS configuration allows the local frontend origins used in the course workflow.

## Run verification

Model verification:

```bash
python -m tests.verify_a
```

Full pytest suite:

```bash
pytest tests/ -v
```

Expected result in the prepared project:

```text
31 passed
```

## Five-minute final submission check

Before pushing the public repository:

1. Start the backend and frontend.
2. Create a task with a past due date and confirm the Overdue pill appears.
3. Use the overdue filter and confirm only overdue tasks remain.
4. Search by title or description and combine it with priority or status.
5. Drag `ToDo -> InProgress` and confirm the PATCH succeeds.
6. Try `Done -> ToDo` and confirm the card reverts with the server message.
7. Run `pytest tests/ -v` and save the output.
8. Confirm the branch is `mid-course-project`.
9. Confirm the repository is public and contains no secrets.

## Documentation

The required course evidence is in [`docs/midcourse/`](docs/midcourse/):

- User stories and acceptance criteria
- Mini-ADR
- Prompt log
- Verification and Break Test evidence
- Reflection
