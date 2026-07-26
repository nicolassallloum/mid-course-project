# Verification Evidence

## Environment

- Python: 3.13
- FastAPI TestClient + pytest
- Frontend verification: headless Chromium interacting with the exact `frontend/index.html` source and a live FastAPI server on port 8000
- Branch: `mid-course-project`

The execution environment blocked direct browser navigation to local URLs, so the exact HTML source was loaded into headless Chromium while its real JavaScript sent requests to the live backend. UI controls, modal flows, drag-and-drop, API persistence, rollback, and screenshots were still exercised through the browser DOM and Fetch API.

## 1. Baseline check before feature verification

The original Module 2 behavior subset was run separately before evaluating the new feature tests.

```text
18 passed in 0.08s
```

Covered baseline behaviors:

- `/health` returns 200.
- Valid create returns 201.
- Missing, blank, invalid, and extra fields return 422.
- Empty and filtered task lists return 200.
- GET by id returns 200 or 404.
- Partial PATCH preserves unrelated fields.
- Valid transitions pass; invalid and same-status transitions return 422.
- DELETE returns 204 with an empty body or 404 when missing.

## 2. Model verification

Command:

```bash
python -m tests.verify_a
```

Expected checks:

- Whitespace title rejected.
- Empty title rejected.
- Title over 200 characters rejected.
- Defaults applied.
- Extra fields rejected.
- `id` rejected on create.
- `created_at` rejected on update.
- Invalid status rejected.

## 3. Full backend test result

Command:

```bash
pytest tests/ -v
```

Final result after implementation and focused refactor:

```text
31 passed in 0.12s
```

The suite contains the 18 preserved baseline tests plus 13 focused tests for the two new features.

### New due-date tests

- Valid due date accepted.
- Invalid date format rejected with 422.
- Past-due active task marked overdue.
- Due date updated through PATCH.
- Overdue filter returns only overdue tasks.
- Completed past-due task is not overdue.
- Due date survives an unrelated update.

### New search/filter tests

- Case-insensitive title search.
- Description search.
- Search combined with status and priority.
- No matches return 200 with `[]`.
- Assignee filter is case-insensitive.
- Invalid enum filter returns 422.

## 4. Live API checks

A live Uvicorn process was used for direct HTTP verification.

```text
health: HTTP 200 | {"status": "ok"}
create overdue: HTTP 201 | due_date returned and is_overdue=true
create future: HTTP 201 | due_date returned and is_overdue=false
search: HTTP 200 | ["Architecture Search Demo"]
overdue filter: HTTP 200 | ["Overdue API Demo"]
combined search + priority + overdue: HTTP 200 | ["Overdue API Demo"]
invalid ToDo -> Done transition: HTTP 422
valid ToDo -> InProgress transition: HTTP 200
```

## 5. Browser checks before refactor

All checks passed against the live backend:

1. Three Kanban columns rendered.
2. Blank title was blocked before any POST request.
3. An overdue task was created and displayed an Overdue pill.
4. A second task was created and the board refreshed.
5. Search filtered the cards while preserving all three columns.
6. The overdue-only filter returned the overdue task only.
7. Dragging `ToDo -> InProgress` sent PATCH and persisted.
8. Dragging `InProgress -> Done` sent PATCH and persisted.
9. Dragging `Done -> ToDo` returned 422, restored the card, and showed the server message.
10. The edit modal updated due date and priority while omitting unchanged status.

## 6. Behavior contract before/after refactor

A working checkpoint was committed before refactoring:

```text
39a732b Implement due dates and combined search filters
```

The refactor extracted small `_matches_search` and `_matches_assignee` helpers from `get_all_tasks`. It did not change route paths, request shapes, enum values, UI selectors, or business rules.

| ID | Behavior contract | Before | After |
|---|---|---:|---:|
| BC-1 | Three columns and counts render | PASS | PASS |
| BC-2 | Cards remain priority sorted | PASS | PASS |
| BC-3 | Loading/empty/error behavior remains available | PASS | PASS |
| BC-4 | Valid drag sends PATCH and persists | PASS | PASS |
| BC-5 | Invalid drag rolls back and shows 422 message | PASS | PASS |
| BC-6 | Create/edit modal and title trimming work | PASS | PASS |
| BC-7 | Due-date display and overdue filter work | PASS | PASS |
| BC-8 | Search and combined filters work | PASS | PASS |

After-refactor verification:

```text
31 passed in 0.12s
```

The same 10 headless-browser checks also passed after the refactor.

## 7. Break Test evidence

### Break Test A — Due-date validation

**Intentional break:** Changed `due_date` from Pydantic `date` to plain `str`.

**Expected protected behavior:** Invalid date input must return HTTP 422.

**Observed result:**

```text
FAILED test_create_task_invalid_due_date_format_returns_422
```

The request reached storage with `"31-12-2030"` as a string and failed instead of being rejected during Pydantic validation. This proved the test protects server-side date validation.

**Restoration:** Reinstated `Optional[date]`, then reran the full suite successfully.

### Break Test B — Search predicate

**Intentional break:** Disabled the `q` search condition in storage.

**Expected protected behavior:** Searching `architecture` should return one matching task.

**Observed result:**

```text
FAILED test_search_matches_title_case_insensitively
Expected: ["Prepare Architecture Diagram"]
Actual:   ["Prepare Architecture Diagram", "Write tests"]
```

This proved the test detects when the backend stops applying text search.

**Restoration:** Restored the search predicate, then reran the full suite successfully.

## 8. Screenshot evidence

- [Board with due-date cards](screenshots/01-board-with-feature-cards.png)
- [Search filter result](screenshots/02-search-filter.png)
- [Overdue-only filter result](screenshots/03-overdue-filter.png)
- [Invalid drag rollback and server message](screenshots/04-invalid-drag-rollback.png)

## 9. Final submission verification

- [x] Two scoped features implemented end-to-end.
- [x] Both features are visible and usable in the frontend.
- [x] Existing behaviors preserved.
- [x] At least four new pytest tests added; 13 were added.
- [x] Full suite passes.
- [x] Two Break Tests documented.
- [x] Behavior contract passed before and after a focused refactor.
- [x] Required documentation exists in `docs/midcourse/`.
- [x] README explains backend, frontend, and test commands.
- [x] No secrets or credentials included.
