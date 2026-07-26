# AI Prompt Log

This log records meaningful AI-assisted steps rather than full chat transcripts. Each entry summarizes the prompt, the draft returned, and the decision to accept, edit, or reject.

## Feature 1 — Due Dates + Overdue Filter

### DD Prompt 1 — Weak prompt rewritten

**Weak prompt**

> Add due dates to my task tracker.

**Why it was weak**

It did not specify files, date format, overdue semantics, frontend behavior, tests, or what existing functionality had to remain unchanged.

**Stronger prompt**

> Work only in `app/models.py` and `app/storage.py`. Add optional `due_date` support using Pydantic v2 `date` validation. Preserve all existing fields, enum values, extra-field rejection, and storage helper names. Compute overdue as `due_date < today` only when status is not `Done`. Do not add a database, scheduler, new routes, or frontend code yet. Return a focused diff and list the tests I should run.

**AI result and decision**

The AI proposed model fields and an overdue helper. I **accepted** the Pydantic date type and helper structure. I **edited** the first draft because it marked completed tasks overdue. I **rejected** a suggestion to store an editable overdue flag.

### DD Prompt 2 — Extend API behavior and tests

**Prompt**

> Extend the existing `GET /tasks` route and storage filter with `overdue: bool | None`. Keep no-match behavior as HTTP 200 with `[]`. Add focused pytest tests for valid due dates, invalid formats, overdue filtering, completed past-due tasks, and preserving a due date after an unrelated PATCH. Do not change route paths or status-transition rules.

**AI result and decision**

The AI drafted the query parameter and tests. I **accepted** the combined filtering approach and test names. I **edited** one test so a task reached `Done` through the valid `ToDo -> InProgress -> Done` sequence instead of bypassing business rules.

### DD Prompt 3 — Add frontend due-date flow

**Prompt**

> Modify only the due-date portions of `frontend/index.html`. Add a date input to the existing create/edit modal, prefill it in edit mode, send `YYYY-MM-DD` or `null`, display the date on cards, and show an Overdue pill only when the API returns `is_overdue=true`. Preserve drag-and-drop, priority sorting, loading/empty/error states, title `.trim()` validation, and 422 handling. Return a focused diff.

**AI result and decision**

The AI added the field, payload mapping, and card pill. I **accepted** the visible UI changes. I **edited** the edit payload so unchanged fields are omitted, avoiding an invalid same-status PATCH.

### DD Prompt 4 — Break Test analysis

**Prompt**

> I intentionally changed `due_date` from a Pydantic `date` field to a plain string. The invalid-date pytest test now fails. Do not repair production code yet. Explain what behavior the test protected and what I should restore.

**AI result and decision**

The AI correctly identified that the test protects server-side date validation. I **accepted** the analysis and restored the typed date field before rerunning the suite.

---

## Feature 2 — Search + Combined Filters

### SF Prompt 1 — Weak prompt rewritten

**Weak prompt**

> Add a search bar and filters.

**Why it was weak**

It allowed the AI to invent client-only filtering, new routes, fuzzy search, frameworks, or hidden-column behavior.

**Stronger prompt**

> Extend the existing `GET /tasks` path only. Add optional `q`, `status`, `priority`, `assignee`, and `overdue` filters. Search `title` and `description` case-insensitively. Apply all supplied filters together. Invalid enums must remain FastAPI/Pydantic 422 responses, and no matches must return 200 with `[]`. Preserve existing storage functions and in-memory design. Do not create a new search endpoint.

**AI result and decision**

The AI returned a combined-filter implementation. I **accepted** the AND behavior and query parameters. I **rejected** a separate `/tasks/search` endpoint and browser-only filtering.

### SF Prompt 2 — Generate focused tests

**Prompt**

> Add focused pytest tests for title search, description search, case-insensitive matching, search combined with status and priority, no-match 200 `[]`, case-insensitive assignee filtering, and invalid enum 422. Use the real TestClient and in-memory reset fixture. Do not mock storage or weaken existing tests.

**AI result and decision**

The AI generated the requested cases. I **accepted** the focused tests. I **edited** the combined-filter setup so the selected task moved to `InProgress` through the public PATCH API.

### SF Prompt 3 — Add compact frontend controls

**Prompt**

> In the existing Kanban header area, add search, status, priority, overdue-only, and Clear controls. Build query parameters for `GET /tasks`; do not filter the main task list independently in JavaScript. Keep all three columns visible, preserve empty placeholders and counts, debounce text search briefly, and do not modify drag-and-drop or modal functions except where needed to refresh results.

**AI result and decision**

The AI added the controls and query builder. I **accepted** the overall structure. I **edited** the empty-result handling to keep all three status columns visible instead of replacing the board with one blank message.

### SF Prompt 4 — Break Test analysis

**Prompt**

> I intentionally disabled the `q` condition in the storage filter. `test_search_matches_title_case_insensitively` expected one task but received both tasks. Analyze the failure without weakening the assertion. Identify the smallest production fix.

**AI result and decision**

The AI correctly traced the failure to the disabled search predicate. I **accepted** the diagnosis, restored the search condition, and reran the full suite.
