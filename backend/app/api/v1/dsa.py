from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import DSAProblem
from app.schemas.schemas import DSAProblemCreate, DSAProblemResponse

router = APIRouter(prefix="/dsa", tags=["DSA"])

@router.get("", response_model=List[DSAProblemResponse])
def get_dsa_problems(db: Session = Depends(get_db)):
    return db.query(DSAProblem).order_by(DSAProblem.id.desc()).all()

@router.post("/problems", response_model=DSAProblemResponse, status_code=status.HTTP_201_CREATED)
def add_dsa_problem(problem_in: DSAProblemCreate, db: Session = Depends(get_db)):
    prob = DSAProblem(**problem_in.dict())
    db.add(prob)
    db.commit()
    db.refresh(prob)
    return prob

@router.get("/summary")
def get_dsa_summary(db: Session = Depends(get_db)):
    total = db.query(DSAProblem).count()
    easy = db.query(DSAProblem).filter(DSAProblem.difficulty == "Easy", DSAProblem.status == "solved").count()
    medium = db.query(DSAProblem).filter(DSAProblem.difficulty == "Medium", DSAProblem.status == "solved").count()
    hard = db.query(DSAProblem).filter(DSAProblem.difficulty == "Hard", DSAProblem.status == "solved").count()
    
    return {
        "total_recorded": total,
        "easy_solved": easy,
        "medium_solved": medium,
        "medium_minimum_target": 50,
        "medium_stretch_target": 60,
        "hard_solved": hard,
        "medium_progress_pct": round((medium / 50.0) * 100.0, 1)
    }
