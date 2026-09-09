from sqlalchemy.orm import Session
from app.models.models import PlannerDay, PlannerTask, TaskCompletion, DailyLog
from app.services.today import get_current_date_str

def calculate_daily_score(db: Session, date_str: str) -> dict:
    planner_day = db.query(PlannerDay).filter(PlannerDay.date == date_str).first()
    if not planner_day:
        return {"score": 0.0, "reasons": ["No planner day found for this date."]}

    tasks = db.query(PlannerTask).filter(PlannerTask.day_number == planner_day.day_number).all()
    if not tasks:
        return {"score": 0.0, "reasons": ["No tasks scheduled for this day."]}

    completions = db.query(TaskCompletion).filter(TaskCompletion.date == date_str).all()
    completion_map = {c.task_id: c for c in completions}

    total_tasks = len(tasks)
    completed_tasks = 0
    critical_completed = 0
    total_critical = sum(1 for t in tasks if t.is_critical)

    total_planned_mins = sum(t.planned_minutes for t in tasks)
    total_actual_mins = 0

    reasons = []

    for t in tasks:
        comp = completion_map.get(t.id)
        if comp:
            total_actual_mins += comp.actual_minutes
            if comp.status == "COMPLETED":
                completed_tasks += 1
                if t.is_critical:
                    critical_completed += 1

    # Base score out of 10
    task_completion_ratio = completed_tasks / total_tasks if total_tasks > 0 else 0
    critical_ratio = critical_completed / total_critical if total_critical > 0 else 1.0
    time_ratio = min(1.0, total_actual_mins / total_planned_mins) if total_planned_mins > 0 else 0

    # Weighted score: 40% task completion, 40% critical tasks, 20% time spent
    raw_score = (task_completion_ratio * 4.0) + (critical_ratio * 4.0) + (time_ratio * 2.0)
    final_score = round(min(10.0, max(0.0, raw_score)), 1)

    if completed_tasks == total_tasks:
        reasons.append("+ All planned tasks completed")
    else:
        reasons.append(f"+ Completed {completed_tasks}/{total_tasks} planned tasks")

    if total_critical > 0:
        if critical_completed == total_critical:
            reasons.append("+ All critical tasks completed")
        else:
            reasons.append(f"- Missed {total_critical - critical_completed} critical task(s)")

    if total_actual_mins < total_planned_mins:
        reasons.append(f"- {total_planned_mins - total_actual_mins} min planned study missed")

    return {
        "score": final_score,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "critical_completed": critical_completed,
        "total_critical": total_critical,
        "planned_minutes": total_planned_mins,
        "actual_minutes": total_actual_mins,
        "reasons": reasons
    }
