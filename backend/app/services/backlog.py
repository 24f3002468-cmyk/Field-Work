from sqlalchemy.orm import Session
from app.models.models import PlannerDay, PlannerTask, TaskCompletion
from app.services.today import get_current_date_str

def get_backlog_summary(db: Session):
    today_date = get_current_date_str()
    
    # Get all past planner days up to yesterday
    past_days = db.query(PlannerDay).filter(PlannerDay.date < today_date).all()
    past_day_numbers = [d.day_number for d in past_days]
    
    if not past_day_numbers:
        return {
            "overdue_count": 0,
            "overdue_hours": 0.0,
            "overdue_tasks": [],
            "critical_overdue_tasks": [],
            "backlog_by_category": {},
            "catch_up_recommendation": "All up to date! Great job staying on track."
        }

    past_tasks = db.query(PlannerTask).filter(PlannerTask.day_number.in_(past_day_numbers)).all()
    past_task_ids = [t.id for t in past_tasks]
    
    completions = db.query(TaskCompletion).filter(TaskCompletion.task_id.in_(past_task_ids)).all()
    completion_map = {c.task_id: c for c in completions}

    overdue_tasks = []
    critical_overdue = []
    backlog_by_cat = {}
    total_missed_minutes = 0

    for t in past_tasks:
        comp = completion_map.get(t.id)
        status = comp.status if comp else "NOT_STARTED"
        
        if status in ["NOT_STARTED", "IN_PROGRESS", "MISSED", "PARTIALLY_COMPLETED"]:
            actual_mins = comp.actual_minutes if comp else 0
            missed_mins = max(0, t.planned_minutes - actual_mins)
            
            if missed_mins > 0 or status in ["NOT_STARTED", "MISSED"]:
                item = {
                    "task_id": t.id,
                    "day_number": t.day_number,
                    "category": t.category,
                    "name": t.name,
                    "planned_minutes": t.planned_minutes,
                    "actual_minutes": actual_mins,
                    "missed_minutes": missed_mins,
                    "is_critical": t.is_critical,
                    "status": status
                }
                overdue_tasks.append(item)
                total_missed_minutes += missed_mins
                
                if t.is_critical:
                    critical_overdue.append(item)
                    
                backlog_by_cat[t.category] = backlog_by_cat.get(t.category, 0) + missed_mins

    # Generate catch-up recommendation
    rec = "No major backlog detected."
    if total_missed_minutes > 0:
        hrs = round(total_missed_minutes / 60.0, 1)
        top_cat = max(backlog_by_cat, key=backlog_by_cat.get) if backlog_by_cat else "DSA"
        rec = f"You are currently {hrs} hours behind schedule. Priority catch-up focus: {top_cat}. Utilize weekend study blocks for recovery without altering daily routine."

    return {
        "overdue_count": len(overdue_tasks),
        "overdue_hours": round(total_missed_minutes / 60.0, 1),
        "overdue_tasks": overdue_tasks,
        "critical_overdue_tasks": critical_overdue,
        "backlog_by_category": backlog_by_cat,
        "catch_up_recommendation": rec
    }
