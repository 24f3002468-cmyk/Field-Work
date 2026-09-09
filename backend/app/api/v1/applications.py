from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Application
from app.schemas.schemas import ApplicationCreate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.application_date.desc()).all()

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    app = Application(**app_in.dict())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.put("/{id}", response_model=ApplicationResponse)
def update_application(id: int, app_in: ApplicationCreate, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"Application {id} not found.")
    
    for key, val in app_in.dict().items():
        setattr(app, key, val)
        
    db.commit()
    db.refresh(app)
    return app

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(id: int, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"Application {id} not found.")
    db.delete(app)
    db.commit()
    return None
