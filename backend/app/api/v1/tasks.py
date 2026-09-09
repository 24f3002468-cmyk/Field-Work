from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import PlannerTask, TaskCompletion
from app.schemas.schemas import TaskCompletionCreate, TaskCompletionResponse
from app.services.backlog import get_backlog_summary

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/today")
def get_today_tasks(db: Session = Depends(get_db)):
    from app.services.today import resolve_today
    return resolve_today(db)["tasks"]

@router.post("/{task_id}/complete", response_model=TaskCompletionResponse)
def complete_task(task_id: str, comp_in: TaskCompletionCreate, db: Session = Depends(get_db)):
    task = db.query(PlannerTask).filter(PlannerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found.")

    comp = db.query(TaskCompletion).filter(TaskCompletion.task_id == task_id, TaskCompletion.date == comp_in.date).first()
    if not comp:
        comp = TaskCompletion(task_id=task_id, date=comp_in.date)
        db.add(comp)

    comp.actual_minutes = comp_in.actual_minutes
    comp.status = comp_in.status
    comp.completion_percentage = comp_in.completion_percentage
    comp.notes = comp_in.notes

    db.commit()
    db.refresh(comp)

    # Write verification: read-after-write assertion
    verified = db.query(TaskCompletion).filter(TaskCompletion.id == comp.id).first()
    if not verified or verified.status != comp_in.status:
        db.rollback()
        raise HTTPException(status_code=500, detail="Write verification failed for task completion.")

    return verified

@router.get("/backlog")
def get_backlog(db: Session = Depends(get_db)):
    return get_backlog_summary(db)
