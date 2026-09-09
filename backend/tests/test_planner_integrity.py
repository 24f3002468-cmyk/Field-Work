import os
import json
import pytest
from datetime import datetime, timedelta

PLANNER_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "planner", "planner_data.json")

def test_planner_file_exists():
    assert os.path.exists(PLANNER_JSON), "planner_data.json must exist."

def test_planner_200_days_integrity():
    with open(PLANNER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    assert len(days) == 200, f"Expected 200 execution days, found {len(days)}."

    day_numbers = [d["day_number"] for d in days]
    assert day_numbers == list(range(1, 201)), "Day numbers must be strictly sequential 1..200."

    # Day 1 must be 2026-09-10
    assert days[0]["date"] == "2026-09-10", f"Day 1 must be 2026-09-10, got {days[0]['date']}"

    # Day 200 date math check
    start_dt = datetime(2026, 9, 10)
    expected_end = (start_dt + timedelta(days=199)).strftime("%Y-%m-%d")
    assert days[-1]["date"] == expected_end, f"Day 200 date mismatch: expected {expected_end}, got {days[-1]['date']}"

def test_project_shipping_deadline_milestone():
    with open(PLANNER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    milestones = data.get("milestones", [])
    ship_m = next((m for m in milestones if m["name"] == "PROJECT 1 SHIPPING DEADLINE"), None)
    assert ship_m is not None, "PROJECT 1 SHIPPING DEADLINE milestone must exist."
    assert ship_m["target_date"] == "2026-12-22", f"Shipping deadline must be 2026-12-22, got {ship_m['target_date']}"

def test_college_schedule_restriction():
    with open(PLANNER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for day in data.get("days", []):
        for task in day.get("tasks", []):
            start = task.get("planned_start")
            end = task.get("planned_end")
            if start and end:
                # No study task should fall between 09:00 and 16:00
                assert not ("09:00" <= start < "16:00"), f"Study task {task['name']} scheduled during college hours (09:00-16:00) on Day {day['day_number']}."
