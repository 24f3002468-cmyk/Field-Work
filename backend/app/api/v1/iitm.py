from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import IITMTask
from app.schemas.schemas import IITMTaskCreate, IITMTaskResponse

router = APIRouter(prefix="/iitm", tags=["IITM"])

@router.get("", response_model=List[IITMTaskResponse])
def get_iitm_tasks(db: Session = Depends(get_db)):
    return db.query(IITMTask).order_by(IITMTask.due_date).all()

@router.post("/tasks", response_model=IITMTaskResponse, status_code=status.HTTP_201_CREATED)
def add_iitm_task(task_in: IITMTaskCreate, db: Session = Depends(get_db)):
    t = IITMTask(**task_in.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.put("/tasks/{id}", response_model=IITMTaskResponse)
def update_iitm_task(id: int, completed: bool, status: str = "Submitted", db: Session = Depends(get_db)):
    t = db.query(IITMTask).filter(IITMTask.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail=f"IITM Task {id} not found.")
    
    t.completed = completed
    t.submission_status = status
    db.commit()
    db.refresh(t)
    return t
