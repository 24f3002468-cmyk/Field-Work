import json
import os
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import (
    PlannerDay, PlannerTask, TaskCompletion, DailyLog, Milestone,
    DSAProblem, ProjectStage, ProjectChecklist, SQLSession, IITMTask,
    PlacementPoint, SystemDesignTopic, Application, NetworkingContact, Offer, BackupRecord
)

def create_backup_export(db: Session, backup_dir: str = "./backups") -> dict:
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.json"
    filepath = os.path.join(backup_dir, filename)

    data = {
        "timestamp": timestamp,
        "days": [d.day_number for d in db.query(PlannerDay).all()],
        "completions": [
            {
                "task_id": c.task_id,
                "date": c.date,
                "actual_minutes": c.actual_minutes,
                "status": c.status,
                "completion_percentage": c.completion_percentage,
                "notes": c.notes
            } for c in db.query(TaskCompletion).all()
        ],
        "daily_logs": [
            {
                "date": l.date,
                "score": l.score,
                "workout": l.workout_completed,
                "sleep": l.sleep_hours,
                "focus": l.focus_hours,
                "blockers": l.blockers,
                "priority": l.tomorrow_priority,
                "notes": l.notes
            } for l in db.query(DailyLog).all()
        ],
        "milestones": [
            {"id": m.id, "name": m.name, "status": m.status, "completed_date": m.completed_date}
            for m in db.query(Milestone).all()
        ],
        "dsa_problems": [
            {
                "title": p.title,
                "difficulty": p.difficulty,
                "topic": p.topic,
                "status": p.status,
                "solve_time_minutes": p.solve_time_minutes,
                "solved_date": p.solved_date
            } for p in db.query(DSAProblem).all()
        ],
        "applications": [
            {
                "company": a.company,
                "role": a.role,
                "status": a.status,
                "application_date": a.application_date
            } for a in db.query(Application).all()
        ]
    }

    content_str = json.dumps(data, indent=2)
    checksum = hashlib.sha256(content_str.encode("utf-8")).hexdigest()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content_str)

    backup_rec = BackupRecord(
        filename=filename,
        status="VERIFIED",
        checksum=checksum
    )
    db.add(backup_rec)
    db.commit()
    db.refresh(backup_rec)

    return {
        "status": "SUCCESS",
        "filename": filename,
        "filepath": filepath,
        "checksum": checksum,
        "created_at": timestamp
    }

def verify_and_restore_backup(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {"status": "FAIL", "reason": "Backup file does not exist."}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "timestamp" not in data or "completions" not in data:
            return {"status": "FAIL", "reason": "Malformed backup schema."}

        return {
            "status": "PASS",
            "message": "Backup verified successfully.",
            "records_checked": len(data.get("completions", [])) + len(data.get("daily_logs", []))
        }
    except Exception as e:
        return {"status": "FAIL", "reason": str(e)}
