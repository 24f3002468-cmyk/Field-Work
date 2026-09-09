from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.verification import run_data_integrity_check, recalculate_metrics
from app.services.backup import create_backup_export

router = APIRouter(prefix="/verification", tags=["Verification"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "HEALTHY", "database": "CONNECTED"}

@router.get("/data-integrity")
def data_integrity(db: Session = Depends(get_db)):
    return run_data_integrity_check(db)

@router.post("/recalculate")
def recalculate(db: Session = Depends(get_db)):
    return recalculate_metrics(db)

@router.get("/backup-status")
def backup_status(db: Session = Depends(get_db)):
    return create_backup_export(db)
