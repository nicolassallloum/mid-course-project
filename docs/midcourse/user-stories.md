# User Stories and Acceptance Criteria

## Feature 1 — Due Dates + Overdue Filter

### Story DD-1 — Set a due date when creating a task

**As a** Task Tracker user,  
**I want** to assign an optional due date while creating a task,  
**so that** I can understand when the work should be completed.

**Acceptance criteria**

- The create modal contains an optional due-date field.
- The frontend sends the date as `YYYY-MM-DD` or sends `null` when it is empty.
- `POST /tasks` accepts a valid ISO date and returns it in `due_date`.
- An invalid date format returns HTTP 422.
- A task with no due date remains valid.

### Story DD-2 — Edit or clear an existing due date

**As a** Task Tracker user,  
**I want** to update or clear a task's due date,  
**so that** the schedule stays accurate when plans change.

**Acceptance criteria**

- The edit modal is prefilled with the task's current due date.
- `PATCH /tasks/{id}` can update `due_date` without changing unrelated fields.
- Sending `null` clears the due date.
- A due date is preserved after an unrelated update.
- The board refreshes after a successful edit.

### Story DD-3 — Identify overdue work visually

**As a** Task Tracker user,  
**I want** overdue tasks to be visually marked,  
**so that** I can prioritize delayed work.

**Acceptance criteria**

- The API returns `is_overdue` for each task.
- A task is overdue when `due_date < today` and status is not `Done`.
- A completed task is not marked overdue, even if its date is in the past.
- An overdue card displays an **Overdue** pill.
- The card still shows its due date.

### Story DD-4 — Filter the board to overdue tasks

**As a** Task Tracker user,  
**I want** an overdue-only filter,  
**so that** I can focus on delayed tasks.

**Acceptance criteria**

- `GET /tasks?overdue=true` returns overdue tasks only.
- The frontend has an **Overdue only** control.
- All three columns remain visible after the filter is applied.
- Clearing filters restores the normal board.
- No matches return HTTP 200 with an empty list.

**AI assumption corrected for Feature 1**

The first AI design suggestion treated every past due date as overdue, including completed tasks. I corrected the rule so `Done` tasks are intentionally excluded from overdue status. This keeps the indicator aligned with actionable work instead of historical lateness.

---

## Feature 2 — Search + Combined Filters

### Story SF-1 — Search by title

**As a** Task Tracker user,  
**I want** to search tasks by title,  
**so that** I can find a specific item quickly.

**Acceptance criteria**

- `GET /tasks?q=...` performs a case-insensitive title search.
- Leading and trailing query whitespace is ignored.
- Matching tasks return HTTP 200.
- No matches return HTTP 200 with `[]`.
- The frontend search field refreshes the board after a short delay.

### Story SF-2 — Search by description

**As a** Task Tracker user,  
**I want** search to include task descriptions,  
**so that** I can find work when I remember details but not the exact title.

**Acceptance criteria**

- Search checks both `title` and `description`.
- Search is case-insensitive.
- The UI renders only returned matches.
- Empty columns remain visible with placeholders.

### Story SF-3 — Combine search with status and priority

**As a** Task Tracker user,  
**I want** to combine text search with status and priority filters,  
**so that** I can narrow a large board precisely.

**Acceptance criteria**

- `q`, `status`, and `priority` can be supplied in the same GET request.
- All supplied conditions are applied together.
- Invalid enum values return HTTP 422.
- The UI provides search, status, and priority controls.
- The column counts represent the filtered result.

### Story SF-4 — Clear active filters

**As a** Task Tracker user,  
**I want** one action that clears all filters,  
**so that** I can return to the full board quickly.

**Acceptance criteria**

- The Clear button resets search, status, priority, and overdue controls.
- The frontend requests the unfiltered task list.
- The normal priority order remains High, Medium, Low.
- Existing drag-and-drop and modal behavior remain available.

**AI assumption corrected for Feature 2**

The initial AI suggestion filtered only in the browser after loading every task. I rejected that approach and implemented search and combined filters in `GET /tasks`, while the frontend builds query parameters. This makes the behavior testable through the API and avoids duplicating filter rules in two places.
