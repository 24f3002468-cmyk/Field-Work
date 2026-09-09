from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import ProjectStage, ProjectChecklist
from app.schemas.schemas import ProjectStageResponse, ProjectChecklistResponse
from datetime import datetime

router = APIRouter(prefix="/project", tags=["Project 1"])

@router.get("", response_model=List[ProjectStageResponse])
def get_project_stages(db: Session = Depends(get_db)):
    return db.query(ProjectStage).order_by(ProjectStage.stage_number).all()

@router.put("/stage/{stage_number}", response_model=ProjectStageResponse)
def update_project_stage(stage_number: int, status: str, db: Session = Depends(get_db)):
    stage = db.query(ProjectStage).filter(ProjectStage.stage_number == stage_number).first()
    if not stage:
        raise HTTPException(status_code=404, detail=f"Project stage {stage_number} not found.")
    
    stage.status = status
    if status == "COMPLETED":
        stage.completed_date = datetime.utcnow().strftime("%Y-%m-%d")
    db.commit()
    db.refresh(stage)
    return stage

@router.get("/checklist", response_model=List[ProjectChecklistResponse])
def get_project_checklist(db: Session = Depends(get_db)):
    return db.query(ProjectChecklist).order_by(ProjectChecklist.id).all()

@router.put("/checklist/{id}", response_model=ProjectChecklistResponse)
def update_checklist_item(id: int, verified: bool, notes: str = None, db: Session = Depends(get_db)):
    item = db.query(ProjectChecklist).filter(ProjectChecklist.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Checklist item {id} not found.")
    
    item.verified = verified
    if notes is not None:
        item.notes = notes
    db.commit()
    db.refresh(item)
    return item

@router.get("/status")
def get_project_shipping_status(db: Session = Depends(get_db)):
    total_checklist = db.query(ProjectChecklist).count()
    verified_checklist = db.query(ProjectChecklist).filter(ProjectChecklist.verified == True).count()
    
    stages = db.query(ProjectStage).order_by(ProjectStage.stage_number).all()
    completed_stages = [s for s in stages if s.status == "COMPLETED"]
    current_stage = next((s for s in stages if s.status != "COMPLETED"), stages[-1] if stages else None)

    ship_status = "NOT SHIPPED"
    if verified_checklist == total_checklist and len(completed_stages) == len(stages) and total_checklist > 0:
        ship_status = "SHIPPED"
    elif verified_checklist >= total_checklist - 2:
        ship_status = "READY TO SHIP"

    return {
        "deadline": "2026-12-22",
        "current_stage": current_stage.name if current_stage else "None",
        "current_stage_number": current_stage.stage_number if current_stage else 15,
        "stages_completed": len(completed_stages),
        "total_stages": len(stages),
        "checklist_verified": verified_checklist,
        "total_checklist": total_checklist,
        "ship_status": ship_status
    }
