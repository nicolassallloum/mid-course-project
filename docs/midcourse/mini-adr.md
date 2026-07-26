# Mini-ADR — Mid-Course Feature Extension

- **Status:** Accepted
- **Decision date:** 26 July 2026
- **Selected features:** Due Dates + Overdue Filter; Search + Combined Filters

## Context

The project extends the in-memory FastAPI Task Tracker from Modules 1–3. The sprint is limited to two small features that must be implemented end-to-end and must demonstrate the course workflow: plan, constrain, implement in small steps, inspect AI output, verify behavior, test, run Break Tests, and document decisions.

## Decision 1 — Store an optional ISO due date and compute overdue in the backend

`TaskCreate`, `TaskUpdate`, and `TaskResponse` include an optional `due_date`. Pydantic's `date` type validates the ISO input. The API also returns `is_overdue`, computed as:

```text
due_date is before today AND status is not Done
```

The frontend displays the due date and uses the returned `is_overdue` value for the pill. `GET /tasks` accepts an optional `overdue` boolean filter.

### Alternatives considered

1. **Compute overdue only in JavaScript.**  
   Rejected because API tests could not directly prove the rule, and multiple clients could calculate it differently.

2. **Persist `is_overdue` as a user-editable field.**  
   Rejected because it is derived data and would become inconsistent with the due date or status.

3. **Add a database and scheduled overdue job.**  
   Rejected as out of scope. The course project intentionally retains in-memory storage.

## Decision 2 — Implement search and combined filters in `GET /tasks`

The existing list route now accepts:

- `q`
- `status`
- `priority`
- `assignee`
- `overdue`

Search is case-insensitive across title and description. Filters use AND behavior when combined. The frontend creates URL query parameters and renders the returned tasks while keeping all Kanban columns visible.

### Alternatives considered

1. **Load every task and filter only in the browser.**  
   Rejected because it duplicates domain behavior in the frontend and weakens backend test coverage.

2. **Create separate endpoints such as `/tasks/search` and `/tasks/overdue`.**  
   Rejected because the existing `GET /tasks` list route is the smallest and clearest extension point.

3. **Add saved views, pagination, or a full query language.**  
   Rejected as too complex for a 3–4 hour scoped sprint.

## Safety and compatibility

- Existing route paths remain unchanged.
- Existing status-transition rules remain the backend source of truth.
- No framework, authentication, database, or unrelated dependency was introduced.
- The frontend omits unchanged fields during edit PATCH requests, preventing an unchanged status from being treated as an invalid same-status transition.
- The full pytest suite and two deliberate Break Tests are documented in `verification.md`.
