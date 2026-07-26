from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


_tasks: dict[str, TaskResponse] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _is_overdue(due_date: Optional[date], status: TaskStatus) -> bool:
    return due_date is not None and due_date < date.today() and status != TaskStatus.DONE


def _refresh_overdue(task: TaskResponse) -> TaskResponse:
    refreshed = task.model_copy(
        update={"is_overdue": _is_overdue(task.due_date, task.status)}
    )
    _tasks[task.id] = refreshed
    return refreshed


def add_task(payload: TaskCreate) -> TaskResponse:
    now = _now()
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        is_overdue=_is_overdue(payload.due_date, payload.status),
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def _matches_assignee(task: TaskResponse, assignee: Optional[str]) -> bool:
    if not assignee:
        return True
    return (task.assignee or "").strip().casefold() == assignee.strip().casefold()


def _matches_search(task: TaskResponse, query: Optional[str]) -> bool:
    if not query or not query.strip():
        return True
    needle = query.strip().casefold()
    return needle in task.title.casefold() or needle in task.description.casefold()


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
    q: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    tasks = [_refresh_overdue(task) for task in _tasks.values()]
    filtered = [
        task
        for task in tasks
        if (status is None or task.status == status)
        and (priority is None or task.priority == priority)
        and _matches_assignee(task, assignee)
        and _matches_search(task, q)
        and (overdue is None or task.is_overdue is overdue)
    ]
    return sorted(filtered, key=lambda task: (task.created_at, task.id))


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _refresh_overdue(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    current = _tasks.get(task_id)
    if current is None:
        return None

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return _refresh_overdue(current)

    if "description" in changes and changes["description"] is None:
        changes["description"] = ""

    updated_values = current.model_dump()
    updated_values.update(changes)
    updated_values["updated_at"] = _now()
    updated_values["is_overdue"] = _is_overdue(
        updated_values.get("due_date"), updated_values["status"]
    )

    updated = TaskResponse(**updated_values)
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
