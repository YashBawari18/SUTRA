"""
SUTRA Backend — routers/audit.py
================================
Immutable Audit Trail & Verification History (Blueprint Part 17).
Maintains complete institutional accountability:
Every AI retrieval, evidence hash check, investigator merge decision,
and case milestone is permanently logged with actor, role, timestamp,
and forensic details.
"""

import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db, AuditLog
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def get_audit_logs(
    case_id: Optional[str] = "MH/CID/2026/0417",
    action_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Returns the complete chronological audit & verification history.
    Filterable by case ID and action type.
    """
    q = db.query(AuditLog)
    if case_id:
        q = q.filter(AuditLog.case_id == case_id)
    if action_type:
        q = q.filter(AuditLog.action_type == action_type.upper())

    logs = q.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    results = []
    for l in logs:
        results.append({
            "id": l.id,
            "case_id": l.case_id,
            "timestamp": l.timestamp.isoformat() if l.timestamp else None,
            "username": l.username,
            "role": l.role,
            "action_type": l.action_type,
            "target_id": l.target_id,
            "details": json.loads(l.details_json or "{}")
        })

    return {
        "case_id": case_id,
        "total_records": len(results),
        "audit_trail": results
    }
