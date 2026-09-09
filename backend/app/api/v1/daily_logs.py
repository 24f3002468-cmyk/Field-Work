from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import DailyLog
from app.schemas.schemas import DailyLogCreate, DailyLogResponse
from app.services.scoring import calculate_daily_score

router = APIRouter(prefix="/daily-logs", tags=["Daily Logs"])

@router.post("", response_model=DailyLogResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_daily_log(log_in: DailyLogCreate, db: Session = Depends(get_db)):
    existing = db.query(DailyLog).filter(DailyLog.date == log_in.date).first()
    
    # Calculate daily score from actual task completion
    score_data = calculate_daily_score(db, log_in.date)
    computed_score = score_data["score"]

    if not existing:
        log = DailyLog(
            date=log_in.date,
            day_number=log_in.day_number,
            score=computed_score,
            workout_completed=log_in.workout_completed,
            sleep_hours=log_in.sleep_hours,
            focus_hours=log_in.focus_hours,
            blockers=log_in.blockers,
            tomorrow_priority=log_in.tomorrow_priority,
            notes=log_in.notes
        )
        db.add(log)
    else:
        log = existing
        log.score = computed_score
        log.workout_completed = log_in.workout_completed
        log.sleep_hours = log_in.sleep_hours
        log.focus_hours = log_in.focus_hours
        log.blockers = log_in.blockers
        log.tomorrow_priority = log_in.tomorrow_priority
        log.notes = log_in.notes

    db.commit()
    db.refresh(log)
    return log

@router.get("/{date}", response_model=DailyLogResponse)
def get_daily_log(date: str, db: Session = Depends(get_db)):
    log = db.query(DailyLog).filter(DailyLog.date == date).first()
    if not log:
        raise HTTPException(status_code=404, detail=f"No daily log found for date {date}.")
    return log
