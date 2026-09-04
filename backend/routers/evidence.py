"""
SUTRA Backend — routers/evidence.py
===================================
Evidence Vault / Repository endpoints.
Supports cryptographic SHA-256 integrity verification, provenance tracking,
chain of custody inspection, and cross-source correlation.
"""

import json
import hashlib
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, EvidenceItem, AuditLog, Relationship
from auth import require_role, TokenData

router = APIRouter()


class EvidenceCreate(BaseModel):
    case_id: str
    title: str
    source_type: str  # FIR, CDR, BANK_RECORD, SURVEILLANCE, FIELD_REPORT
    source_agency: str = "Maharashtra Police CID"
    officer_name: str = "Insp. V. Kadam"
    content_text: str
    reliability_score: float = 0.9


class IntegrityVerificationResponse(BaseModel):
    evidence_id: str
    title: str
    stored_hash: str
    computed_hash: str
    status: str  # "VERIFIED_AUTHENTIC" or "INTEGRITY_VIOLATION_TAMPERED"
    is_valid: bool
    verified_by: str
    verified_at: str
    message: str


@router.get("")
def list_evidence(
    case_id: str = "MH/CID/2026/0417",
    source_type: str | None = None,
    verified_status: str | None = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Lists all evidence records stored in the Evidence Vault.
    Filterable by case, source type, and verification status.
    """
    q = db.query(EvidenceItem).filter(EvidenceItem.case_id == case_id)
    if source_type:
        q = q.filter(EvidenceItem.source_type == source_type.upper())
    if verified_status:
        q = q.filter(EvidenceItem.verified_status == verified_status.lower())

    items = q.order_by(EvidenceItem.created_at.desc()).all()
    results = []
    for item in items:
        # Calculate how many graph edges cite this evidence item
        rel_count = db.query(Relationship).filter(
            Relationship.case_id == case_id,
            Relationship.evidence_ids.contains(item.evidence_id)
        ).count()

        results.append({
            "evidence_id": item.evidence_id,
            "case_id": item.case_id,
            "title": item.title,
            "source_type": item.source_type,
            "source_agency": item.source_agency,
            "officer_name": item.officer_name,
            "sha256_hash": item.sha256_hash,
            "reliability_score": item.reliability_score,
            "verified_status": item.verified_status,
            "verified_by": item.verified_by,
            "verified_at": item.verified_at.isoformat() if item.verified_at else None,
            "provenance_chain": json.loads(item.provenance_chain or "[]"),
            "linked_relationships_count": rel_count,
            "content_preview": (item.content_text[:140] + "...") if len(item.content_text) > 140 else item.content_text,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })

    return {
        "case_id": case_id,
        "total_items": len(results),
        "evidence_items": results
    }


@router.get("/{evidence_id}")
def get_evidence_item(
    evidence_id: str,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Returns complete text, custody provenance, and linked graph edges for an evidence item.
    """
    item = db.query(EvidenceItem).filter(EvidenceItem.evidence_id == evidence_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Evidence record not found in vault")

    # Find edges referencing this evidence item
    relationships = db.query(Relationship).filter(
        Relationship.evidence_ids.contains(evidence_id)
    ).all()

    linked_edges = [
        {
            "id": r.id,
            "source": r.source_id,
            "target": r.target_id,
            "rel_type": r.rel_type,
            "weight": r.weight,
            "amount": r.amount,
            "timestamp": r.timestamp
        }
        for r in relationships
    ]

    return {
        "evidence_id": item.evidence_id,
        "case_id": item.case_id,
        "title": item.title,
        "source_type": item.source_type,
        "source_agency": item.source_agency,
        "officer_name": item.officer_name,
        "sha256_hash": item.sha256_hash,
        "content_text": item.content_text,
        "reliability_score": item.reliability_score,
        "verified_status": item.verified_status,
        "verified_by": item.verified_by,
        "verified_at": item.verified_at.isoformat() if item.verified_at else None,
        "provenance_chain": json.loads(item.provenance_chain or "[]"),
        "linked_edges": linked_edges,
        "created_at": item.created_at.isoformat() if item.created_at else None
    }


@router.post("/verify-integrity/{evidence_id}", response_model=IntegrityVerificationResponse)
def verify_evidence_integrity(
    evidence_id: str,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Cryptographic SHA-256 integrity verification.
    Recalculates the exact SHA-256 hash of the vault record's content,
    compares against the registered checksum, and records the event in the audit trail.
    """
    item = db.query(EvidenceItem).filter(EvidenceItem.evidence_id == evidence_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Evidence item not found")

    computed_hash = hashlib.sha256(item.content_text.encode("utf-8")).hexdigest()
    is_valid = (computed_hash.lower() == item.sha256_hash.lower())
    now = datetime.now()

    if is_valid:
        status_label = "VERIFIED_AUTHENTIC"
        message = "Cryptographic checksum matches registered vault hash. Document is authentic and unaltered."
        item.verified_status = "verified"
        item.verified_by = user.username
        item.verified_at = now
    else:
        status_label = "INTEGRITY_VIOLATION_TAMPERED"
        message = "WARNING: Computed checksum does NOT match stored vault hash! Possible record tampering."
        item.verified_status = "flagged"

    # Append to immutable Audit Log
    audit_entry = AuditLog(
        case_id=item.case_id,
        timestamp=now,
        username=user.username,
        role=user.role,
        action_type="EVIDENCE_INTEGRITY_VERIFIED",
        target_id=evidence_id,
        details_json=json.dumps({
            "evidence_id": evidence_id,
            "title": item.title,
            "stored_hash": item.sha256_hash,
            "computed_hash": computed_hash,
            "status": status_label,
            "is_valid": is_valid
        })
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(item)

    return IntegrityVerificationResponse(
        evidence_id=item.evidence_id,
        title=item.title,
        stored_hash=item.sha256_hash,
        computed_hash=computed_hash,
        status=status_label,
        is_valid=is_valid,
        verified_by=user.username,
        verified_at=now.isoformat(),
        message=message
    )


@router.post("")
def create_evidence(
    payload: EvidenceCreate,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """Creates a new evidence entry and computes SHA-256 hash automatically."""
    count = db.query(EvidenceItem).count() + 1
    evidence_id = f"EVID-2026-{count:03d}"
    computed_hash = hashlib.sha256(payload.content_text.encode("utf-8")).hexdigest()
    now = datetime.now()

    prov = [
        {"timestamp": now.isoformat(), "actor": user.username, "action": "Deposited into Evidence Vault", "station": payload.source_agency}
    ]

    item = EvidenceItem(
        evidence_id=evidence_id,
        case_id=payload.case_id,
        title=payload.title,
        source_type=payload.source_type.upper(),
        source_agency=payload.source_agency,
        officer_name=payload.officer_name,
        sha256_hash=computed_hash,
        content_text=payload.content_text,
        provenance_chain=json.dumps(prov),
        reliability_score=payload.reliability_score,
        verified_status="verified",
        verified_by=user.username,
        verified_at=now,
        created_at=now
    )
    db.add(item)

    # Log action
    audit = AuditLog(
        case_id=payload.case_id,
        timestamp=now,
        username=user.username,
        role=user.role,
        action_type="EVIDENCE_DEPOSITED",
        target_id=evidence_id,
        details_json=json.dumps({"title": payload.title, "source_type": payload.source_type, "sha256": computed_hash})
    )
    db.add(audit)
    db.commit()
    db.refresh(item)

    return {"message": "Evidence created successfully", "evidence_id": evidence_id, "sha256_hash": computed_hash}
