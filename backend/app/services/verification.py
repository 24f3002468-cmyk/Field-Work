from sqlalchemy.orm import Session
from app.models.models import PlannerDay, PlannerTask, Milestone, DSAProblem, SQLSession, ProjectChecklist, TaskCompletion
from app.services.today import get_current_date_str

def run_data_integrity_check(db: Session) -> dict:
    issues = []
    
    # 1. Verify 200 planner days exist
    days_count = db.query(PlannerDay).count()
    if days_count != 200:
        issues.append(f"Expected 200 planner days, found {days_count}.")

    # 2. Check for duplicate or missing day numbers
    day_numbers = [d.day_number for d in db.query(PlannerDay.day_number).order_by(PlannerDay.day_number).all()]
    expected_numbers = list(range(1, 201))
    missing_days = set(expected_numbers) - set(day_numbers)
    if missing_days:
        issues.append(f"Missing day numbers: {sorted(list(missing_days))}")
        
    if len(day_numbers) != len(set(day_numbers)):
        issues.append("Duplicate day numbers detected in planner_days table.")

    # 3. Verify Day 1 date is 2026-09-10
    day1 = db.query(PlannerDay).filter(PlannerDay.day_number == 1).first()
    if day1 and day1.date != "2026-09-10":
        issues.append(f"Day 1 date mismatch: expected 2026-09-10, found {day1.date}.")

    # 4. Verify Project Shipping Milestone Dec 22, 2026
    ship_m = db.query(Milestone).filter(Milestone.name == "PROJECT 1 SHIPPING DEADLINE").first()
    if ship_m and ship_m.target_date != "2026-12-22":
        issues.append(f"Project shipping deadline mismatch: expected 2026-12-22, found {ship_m.target_date}.")

    # 5. Check task orphan records
    total_tasks = db.query(PlannerTask).count()
    if total_tasks == 0:
        issues.append("No planner tasks found in database.")

    status = "PASS" if not issues else "FAIL"
    
    return {
        "status": status,
        "days_count": days_count,
        "tasks_count": total_tasks,
        "milestones_count": db.query(Milestone).count(),
        "issues_found": len(issues),
        "issues": issues,
        "timestamp": get_current_date_str()
    }

def recalculate_metrics(db: Session) -> dict:
    # Idempotent recalculation of derived progress counters
    dsa_medium_count = db.query(DSAProblem).filter(DSAProblem.difficulty == "Medium", DSAProblem.status == "solved").count()
    
    sql_mins = sum(s.minutes for s in db.query(SQLSession).all())
    sql_hours = round(sql_mins / 60.0, 1)

    completed_checklist = db.query(ProjectChecklist).filter(ProjectChecklist.verified == True).count()
    total_checklist = db.query(ProjectChecklist).count()
    project_pct = round((completed_checklist / total_checklist * 100.0), 1) if total_checklist > 0 else 0.0

    return {
        "status": "SUCCESS",
        "message": "All metrics recalculated idempotently.",
        "recalculated": {
            "dsa_medium_solved": dsa_medium_count,
            "sql_hours_logged": sql_hours,
            "project_completion_percentage": project_pct
        }
    }
