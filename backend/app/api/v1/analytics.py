from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import DailyLog, TaskCompletion, PlannerTask, DSAProblem, SQLSession
from app.services.backlog import get_backlog_summary

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/performance")
def get_performance_analytics(db: Session = Depends(get_db)):
    logs = db.query(DailyLog).order_by(DailyLog.date.desc()).limit(30).all()
    scores = [{"date": l.date, "score": l.score, "focus_hours": l.focus_hours} for l in reversed(logs)]

    backlog = get_backlog_summary(db)
    
    # Load status calculator (transparent, non-medical)
    overdue_hrs = backlog["overdue_hours"]
    recent_focus_avg = sum(l.focus_hours for l in logs[:7]) / max(1, len(logs[:7])) if logs else 0
    
    if overdue_hrs > 10.0 or (logs and len(logs) >= 3 and all(l.score < 5.0 for l in logs[:3])):
        load_status = "RECOVERY NEEDED"
    elif overdue_hrs > 4.0 or recent_focus_avg > 6.0:
        load_status = "HIGH LOAD"
    else:
        load_status = "HEALTHY"

    return {
        "recent_scores": scores,
        "load_status": load_status,
        "load_factors": {
            "overdue_hours": overdue_hrs,
            "recent_daily_focus_average": round(recent_focus_avg, 1)
        },
        "backlog_summary": backlog
    }
