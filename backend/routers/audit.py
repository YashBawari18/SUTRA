from fastapi import APIRouter, Depends
from auth import require_role, TokenData
from database import SessionLocal
from models import AuditLog

router = APIRouter()

@router.get("")
def get_audit_logs(case_id: str | None = None, user: TokenData = Depends(require_role("investigator"))):
    """
    Exposes the immutable audit trail for the UI.
    """
    db = SessionLocal()
    try:
        query = db.query(AuditLog)
        if case_id:
            query = query.filter(AuditLog.case_id == case_id)
        
        logs = query.order_by(AuditLog.timestamp.desc()).all()
        return {"case_id": case_id, "logs": logs}
    finally:
        db.close()

