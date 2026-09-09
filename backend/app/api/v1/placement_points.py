from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import PlacementPoint
from app.schemas.schemas import PlacementPointCreate, PlacementPointResponse

router = APIRouter(prefix="/placement-points", tags=["Placement Points"])

@router.get("", response_model=List[PlacementPointResponse])
def get_placement_points(db: Session = Depends(get_db)):
    return db.query(PlacementPoint).order_by(PlacementPoint.date.desc()).all()

@router.post("", response_model=PlacementPointResponse, status_code=status.HTTP_201_CREATED)
def add_placement_point(point_in: PlacementPointCreate, db: Session = Depends(get_db)):
    p = PlacementPoint(**point_in.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/summary")
def get_placement_points_summary(required_points: int = 50, db: Session = Depends(get_db)):
    points = db.query(PlacementPoint).all()
    earned = sum(p.points for p in points if p.status == "Verified")
    pending = sum(p.points for p in points if p.status == "Pending")
    
    cert_points = sum(p.points for p in points if p.category == "Certificate" and p.status == "Verified")
    ps_points = sum(p.points for p in points if p.category == "Problem Solving" and p.status == "Verified")
    other_points = earned - cert_points - ps_points

    return {
        "required_points": required_points,
        "earned_points": earned,
        "pending_points": pending,
        "remaining_points": max(0, required_points - earned),
        "certificates": cert_points,
        "problem_solving": ps_points,
        "other_activities": other_points,
        "submission_status": "Verified" if earned >= required_points else ("Pending" if pending > 0 else "In Progress")
    }
