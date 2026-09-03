"""SUTRA Backend — routers/audit.py : immutable audit trail (blueprint Part 17)."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def get_audit_logs(case_id: str | None = None, user: TokenData = Depends(require_role("admin"))):
    """
    Every AI-generated suggestion (entity merge, risk score, assistant
    answer) and every investigator action (confirm/reject merge, mark
    finding verified, generate report) must be written here at the point
    it happens, with: actor, action, timestamp, case_id, and before/after
    state where applicable. Admin-only read access.
    """
    return {"case_id": case_id, "logs": []}
