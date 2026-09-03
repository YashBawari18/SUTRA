from fastapi import APIRouter, Depends
from auth import require_role, TokenData
from database import SessionLocal
from models import Evidence

router = APIRouter()

@router.get("/{case_id}")
def list_evidence(case_id: str, user: TokenData = Depends(require_role("investigator"))):
    """
    Retrieves the Evidence Vault for a case, exposing SHA-256 hashes and provenance data.
    """
    db = SessionLocal()
    try:
        evidence = db.query(Evidence).filter(Evidence.case_id == case_id).all()
        return {"case_id": case_id, "evidence_vault": evidence}
    finally:
        db.close()
