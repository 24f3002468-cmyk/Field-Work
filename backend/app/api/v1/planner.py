from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import PlannerDay, PlannerTask, Milestone
from app.schemas.schemas import PlannerDaySchema, MilestoneResponse
from app.services.today import resolve_today

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.get("/today")
def get_today_planner(db: Session = Depends(get_db)):
    return resolve_today(db)

@router.get("/day/{day_number}", response_model=PlannerDaySchema)
def get_planner_day(day_number: int, db: Session = Depends(get_db)):
    day = db.query(PlannerDay).filter(PlannerDay.day_number == day_number).first()
    if not day:
        raise HTTPException(status_code=404, detail=f"Planner day {day_number} not found.")
    return day

@router.get("/week/{week_number}")
def get_planner_week(week_number: int, db: Session = Depends(get_db)):
    start_day = (week_number - 1) * 7 + 1
    end_day = min(200, week_number * 7)
    days = db.query(PlannerDay).filter(PlannerDay.day_number >= start_day, PlannerDay.day_number <= end_day).all()
    return {"week_number": week_number, "start_day": start_day, "end_day": end_day, "days": days}

@router.get("/milestones", response_model=List[MilestoneResponse])
def get_all_milestones(db: Session = Depends(get_db)):
    return db.query(Milestone).order_by(Milestone.target_day).all()
