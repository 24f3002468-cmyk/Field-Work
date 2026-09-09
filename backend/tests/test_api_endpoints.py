import pytest
from fastapi.testclient import TestClient
from app.main import app, seed_database_if_needed

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database_if_needed()

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/verification/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_data_integrity_endpoint():
    response = client.get("/api/v1/verification/data-integrity")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PASS"
    assert data["days_count"] == 200

def test_get_today_planner():
    response = client.get("/api/v1/planner/today")
    assert response.status_code == 200
    data = response.json()
    assert "day_number" in data
    assert "tasks" in data
    assert len(data["tasks"]) > 0

def test_task_completion_write_verification():
    payload = {
        "task_id": "D1-T1",
        "date": "2026-09-10",
        "actual_minutes": 45,
        "status": "COMPLETED",
        "completion_percentage": 100.0,
        "notes": "Solved array 2-pointer problem."
    }
    response = client.post("/api/v1/tasks/D1-T1/complete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["actual_minutes"] == 45

def test_dsa_summary():
    response = client.get("/api/v1/dsa/summary")
    assert response.status_code == 200
    data = response.json()
    assert "medium_minimum_target" in data
    assert data["medium_minimum_target"] == 50

def test_project_status():
    response = client.get("/api/v1/project/status")
    assert response.status_code == 200
    data = response.json()
    assert data["deadline"] == "2026-12-22"
    assert "ship_status" in data

def test_recalculate_idempotency():
    res1 = client.post("/api/v1/verification/recalculate")
    res2 = client.post("/api/v1/verification/recalculate")
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json() == res2.json()
