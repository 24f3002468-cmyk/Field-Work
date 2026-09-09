from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Milestone
from app.schemas.schemas import MilestoneResponse, MilestoneStatusUpdate

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.get("", response_model=List[MilestoneResponse])
def get_milestones(db: Session = Depends(get_db)):
    return db.query(Milestone).order_by(Milestone.target_day).all()

@router.get("/critical", response_model=List[MilestoneResponse])
def get_critical_milestones(db: Session = Depends(get_db)):
    return db.query(Milestone).filter(Milestone.critical == True).order_by(Milestone.target_day).all()

@router.put("/{id}/status", response_model=MilestoneResponse)
def update_milestone_status(id: int, status_in: MilestoneStatusUpdate, db: Session = Depends(get_db)):
    m = db.query(Milestone).filter(Milestone.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail=f"Milestone {id} not found.")
    
    m.status = status_in.status
    if status_in.completed_date:
        m.completed_date = status_in.completed_date
    elif status_in.status == "completed" and not m.completed_date:
        from app.services.today import get_current_date_str
        m.completed_date = get_current_date_str()

    db.commit()
    db.refresh(m)
    return m
