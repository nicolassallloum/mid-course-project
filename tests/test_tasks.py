from datetime import date, timedelta

from fastapi.testclient import TestClient


def create_task(client: TestClient, **overrides) -> dict:
    payload = {"title": "Example task"}
    payload.update(overrides)
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


# Existing Module 2 behavior -------------------------------------------------

def test_health_returns_200(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_valid_returns_201_with_full_body(client: TestClient):
    response = client.post("/tasks", json={"title": "  Build UI  "})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Build UI"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["assignee"] is None
    assert body["due_date"] is None
    assert body["is_overdue"] is False
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client: TestClient):
    assert client.post("/tasks", json={}).status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient):
    assert client.post("/tasks", json={"title": "   "}).status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient):
    assert client.post("/tasks", json={"title": "x", "priority": "Urgent"}).status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient):
    assert client.post("/tasks", json={"title": "x", "unknown": True}).status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient):
    create_task(client)
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient):
    create_task(client, title="high", priority="High")
    create_task(client, title="low", priority="Low")
    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["high"]


def test_get_task_by_id_returns_task(client: TestClient, created_task: dict):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient):
    response = client.get("/tasks/missing")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing not found"


def test_patch_partial_update_keeps_other_fields(client: TestClient):
    task = create_task(client, title="Old", priority="High", assignee="Nix")
    response = client.patch(f"/tasks/{task['id']}", json={"title": "New"})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["priority"] == "High"
    assert body["assignee"] == "Nix"


def test_patch_not_found_returns_404(client: TestClient):
    assert client.patch("/tasks/missing", json={"title": "x"}).status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client: TestClient):
    task = create_task(client)
    response = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client: TestClient):
    task = create_task(client)
    response = client.patch(f"/tasks/{task['id']}", json={"status": "Done"})
    assert response.status_code == 422


def test_patch_same_status_returns_422(client: TestClient):
    task = create_task(client)
    assert client.patch(f"/tasks/{task['id']}", json={"status": "ToDo"}).status_code == 422


def test_delete_existing_returns_204_no_body(client: TestClient):
    task = create_task(client)
    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client: TestClient):
    assert client.delete("/tasks/missing").status_code == 404


# Feature 1: Due dates + overdue filter -------------------------------------

def test_create_task_with_valid_due_date(client: TestClient):
    future = (date.today() + timedelta(days=7)).isoformat()
    task = create_task(client, due_date=future)
    assert task["due_date"] == future
    assert task["is_overdue"] is False


def test_create_task_invalid_due_date_format_returns_422(client: TestClient):
    response = client.post("/tasks", json={"title": "Bad date", "due_date": "31-12-2030"})
    assert response.status_code == 422


def test_past_due_todo_task_is_marked_overdue(client: TestClient):
    past = (date.today() - timedelta(days=1)).isoformat()
    task = create_task(client, title="Late task", due_date=past)
    assert task["is_overdue"] is True


def test_update_due_date(client: TestClient):
    task = create_task(client)
    future = (date.today() + timedelta(days=3)).isoformat()
    response = client.patch(f"/tasks/{task['id']}", json={"due_date": future})
    assert response.status_code == 200
    assert response.json()["due_date"] == future


def test_overdue_filter_returns_only_overdue_tasks(client: TestClient):
    past = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    create_task(client, title="late", due_date=past)
    create_task(client, title="future", due_date=future)
    create_task(client, title="no date")

    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["late"]


def test_done_task_with_past_due_date_is_not_overdue(client: TestClient):
    past = (date.today() - timedelta(days=2)).isoformat()
    task = create_task(client, title="Finished late", due_date=past)
    assert client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"}).status_code == 200
    done = client.patch(f"/tasks/{task['id']}", json={"status": "Done"})
    assert done.status_code == 200
    assert done.json()["is_overdue"] is False


def test_due_date_is_preserved_after_unrelated_update(client: TestClient):
    due = (date.today() + timedelta(days=5)).isoformat()
    task = create_task(client, title="Keep date", due_date=due)
    response = client.patch(f"/tasks/{task['id']}", json={"assignee": "Nicolas"})
    assert response.status_code == 200
    assert response.json()["due_date"] == due


# Feature 2: Search + combined filters --------------------------------------

def test_search_matches_title_case_insensitively(client: TestClient):
    create_task(client, title="Prepare Architecture Diagram")
    create_task(client, title="Write tests")
    response = client.get("/tasks", params={"q": "architecture"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Prepare Architecture Diagram"]


def test_search_matches_description(client: TestClient):
    create_task(client, title="Backend work", description="Add PostgreSQL migration notes")
    response = client.get("/tasks", params={"q": "migration"})
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Backend work"


def test_search_combines_with_status_and_priority(client: TestClient):
    matching = create_task(client, title="Critical API task", priority="High")
    create_task(client, title="Critical UI task", priority="Low")
    create_task(client, title="Other API task", priority="High")
    assert client.patch(f"/tasks/{matching['id']}", json={"status": "InProgress"}).status_code == 200

    response = client.get(
        "/tasks",
        params={"q": "critical", "status": "InProgress", "priority": "High"},
    )
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [matching["id"]]


def test_search_no_matches_returns_200_and_empty_list(client: TestClient):
    create_task(client, title="Existing")
    response = client.get("/tasks", params={"q": "not-present"})
    assert response.status_code == 200
    assert response.json() == []


def test_filter_by_assignee_is_case_insensitive(client: TestClient):
    create_task(client, title="Assigned", assignee="Nicolas")
    create_task(client, title="Other", assignee="Maya")
    response = client.get("/tasks", params={"assignee": "nicolas"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Assigned"]


def test_invalid_filter_enum_returns_422(client: TestClient):
    response = client.get("/tasks", params={"priority": "Urgent"})
    assert response.status_code == 422
