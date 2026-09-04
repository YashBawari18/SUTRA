"""
SUTRA Backend — routers/entities.py
===================================
Extracted Entity Profiles & Human Verification Workflow.
Features:
  - Full entity listing with attributes and roles
  - Pending entity-resolution candidate queue (no silent merges!)
  - Human approval / rejection decision endpoint
  - Automatic audit ledger logging
"""

import json
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Entity, ResolutionCandidate, AuditLog
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def list_entities(
    case_id: str = "MH/CID/2026/0417",
    entity_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """Lists all entities in the case knowledge base."""
    q = db.query(Entity).filter(Entity.case_id == case_id)
    if entity_type:
        q = q.filter(Entity.type == entity_type.lower())

    entities = q.all()
    results = []
    for e in entities:
        attrs = json.loads(e.attributes_json or "{}")
        aliases = json.loads(e.aliases or "[]")
        results.append({
            "id": e.entity_id,
            "label": e.label,
            "type": e.type,
            "role": e.role,
            "aliases": aliases,
            "attributes": attrs,
            "created_at": e.created_at.isoformat() if e.created_at else None
        })
    return {
        "case_id": case_id,
        "total_entities": len(results),
        "entities": results
    }


@router.get("/resolution-candidates")
def list_resolution_candidates(
    case_id: str = "MH/CID/2026/0417",
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Human Verification Workflow:
    Returns entity-resolution candidate suggestions awaiting human approval.
    Enforces SUTRA principle: No silent AI merges without human sign-off.
    """
    q = db.query(ResolutionCandidate).filter(ResolutionCandidate.case_id == case_id)
    if status:
        q = q.filter(ResolutionCandidate.status == status.lower())

    candidates = q.order_by(ResolutionCandidate.id.asc()).all()
    results = []
    for c in candidates:
        results.append({
            "id": c.id,
            "case_id": c.case_id,
            "source_mention": c.source_mention,
            "target_mention": c.target_mention,
            "suggested_entity_id": c.suggested_entity_id,
            "similarity_score": c.similarity_score,
            "confidence": c.confidence,
            "shared_attributes": json.loads(c.shared_attributes or "[]"),
            "status": c.status,
            "reviewed_by": c.reviewed_by,
            "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else None
        })

    return {
        "case_id": case_id,
        "total_candidates": len(results),
        "pending_count": sum(1 for r in results if r["status"] == "pending"),
        "candidates": results
    }


@router.post("/resolution-candidates/{candidate_id}/confirm")
def confirm_resolution_candidate(
    candidate_id: int,
    approve: bool,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Investigator confirms or rejects an entity merge candidate.
    Action is permanently recorded in the immutable audit trail.
    """
    candidate = db.query(ResolutionCandidate).filter(ResolutionCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Resolution candidate not found")

    now = datetime.now()
    action_type = "ENTITY_MERGE_APPROVED" if approve else "ENTITY_MERGE_REJECTED"
    candidate.status = "approved" if approve else "rejected"
    candidate.reviewed_by = user.username
    candidate.reviewed_at = now

    # If approved, attach alias to canonical entity
    if approve and candidate.suggested_entity_id:
        target_entity = db.query(Entity).filter(Entity.entity_id == candidate.suggested_entity_id).first()
        if target_entity:
            curr_aliases = json.loads(target_entity.aliases or "[]")
            if candidate.source_mention not in curr_aliases:
                curr_aliases.append(candidate.source_mention)
                target_entity.aliases = json.dumps(curr_aliases)

    # Log in immutable audit trail
    audit = AuditLog(
        case_id=candidate.case_id,
        timestamp=now,
        username=user.username,
        role=user.role,
        action_type=action_type,
        target_id=candidate.suggested_entity_id or str(candidate.id),
        details_json=json.dumps({
            "candidate_id": candidate.id,
            "source_mention": candidate.source_mention,
            "target_mention": candidate.target_mention,
            "approved": approve,
            "confidence": candidate.confidence
        })
    )
    db.add(audit)
    db.commit()

    return {
        "candidate_id": candidate_id,
        "approved": approve,
        "status": candidate.status,
        "reviewed_by": user.username,
        "reviewed_at": now.isoformat(),
        "message": f"Entity merge successfully {'approved and merged' if approve else 'rejected'}."
    }
