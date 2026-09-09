from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import json
import csv
import io
from app.core.database import get_db
from app.models.models import TaskCompletion, DailyLog, DSAProblem

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/json")
def export_json(db: Session = Depends(get_db)):
    completions = db.query(TaskCompletion).all()
    logs = db.query(DailyLog).all()
    dsa = db.query(DSAProblem).all()

    data = {
        "task_completions": [
            {"task_id": c.task_id, "date": c.date, "actual_minutes": c.actual_minutes, "status": c.status, "notes": c.notes}
            for c in completions
        ],
        "daily_logs": [
            {"date": l.date, "score": l.score, "workout": l.workout_completed, "sleep": l.sleep_hours, "focus": l.focus_hours}
            for l in logs
        ],
        "dsa_problems": [
            {"title": d.title, "difficulty": d.difficulty, "topic": d.topic, "solved_date": d.solved_date}
            for d in dsa
        ]
    }

    return Response(content=json.dumps(data, indent=2), media_type="application/json", headers={"Content-Disposition": "attachment; filename=ml_dashboard_export.json"})

@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Task ID", "Date", "Actual Minutes", "Status", "Notes"])
    
    for c in db.query(TaskCompletion).all():
        writer.writerow([c.task_id, c.date, c.actual_minutes, c.status, c.notes or ""])
        
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=ml_dashboard_tasks.csv"})
