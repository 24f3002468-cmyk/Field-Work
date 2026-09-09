from datetime import datetime
import pytz
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import PlannerDay, TaskCompletion

def get_current_date_str() -> str:
    tz = pytz.timezone(settings.TIMEZONE)
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d")

def get_current_time_str() -> str:
    tz = pytz.timezone(settings.TIMEZONE)
    now = datetime.now(tz)
    return now.strftime("%H:%M")

def resolve_today(db: Session):
    today_date = get_current_date_str()
    planner_day = db.query(PlannerDay).filter(PlannerDay.date == today_date).first()
    
    if not planner_day:
        planner_day = db.query(PlannerDay).filter(PlannerDay.day_number == 1).first()

    tasks = planner_day.tasks if planner_day else []
    
    completion_map = {}
    if planner_day:
        completions = db.query(TaskCompletion).filter(TaskCompletion.date == planner_day.date).all()
        completion_map = {c.task_id: c for c in completions}

    task_summaries = []
    completed_count = 0
    total_planned_minutes = 0
    actual_minutes = 0

    for t in tasks:
        comp = completion_map.get(t.id)
        status = comp.status if comp else "NOT_STARTED"
        mins = comp.actual_minutes if comp else 0
        
        if status == "COMPLETED":
            completed_count += 1
            
        total_planned_minutes += t.planned_minutes
        actual_minutes += mins
        
        task_summaries.append({
            "id": t.id,
            "category": t.category,
            "name": t.name,
            "description": t.description,
            "planned_start": t.planned_start,
            "planned_end": t.planned_end,
            "planned_minutes": t.planned_minutes,
            "actual_minutes": mins,
            "status": status,
            "completion_percentage": comp.completion_percentage if comp else 0.0,
            "is_critical": t.is_critical,
            "priority": t.priority,
            "notes": comp.notes if comp else None
        })

    now_time = get_current_time_str()
    active_task = None
    
    for t in task_summaries:
        if t["planned_start"] and t["planned_end"]:
            if t["planned_start"] <= now_time <= t["planned_end"]:
                active_task = t
                break

    return {
        "today_date": today_date,
        "current_time": now_time,
        "day_number": planner_day.day_number if planner_day else 1,
        "part": planner_day.part if planner_day else 1,
        "phase": planner_day.phase if planner_day else "DSA Foundation",
        "sub_phase": planner_day.sub_phase if planner_day else "",
        "primary_technology": planner_day.primary_technology if planner_day else "",
        "total_tasks": len(tasks),
        "completed_tasks": completed_count,
        "total_planned_minutes": total_planned_minutes,
        "actual_minutes": actual_minutes,
        "tasks": task_summaries,
        "active_task_now": active_task,
        "milestone": planner_day.milestone_name if planner_day else None
    }
