"""SUTRA Backend — routers/upload.py : document ingestion endpoints."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from auth import require_role, TokenData
from database import get_db
from models import Evidence, Case, AuditLog, User
import hashlib
from storage import storage

router = APIRouter()

ALLOWED_TYPES = {".pdf", ".csv", ".txt", ".jpg", ".png"}

@router.post("")
async def upload_document(
    case_id: str = Form(...),
    file: UploadFile = File(...),
    user: TokenData = Depends(require_role("investigator")),
    db: Session = Depends(get_db)
):
    """
    Accepts a source document (FIR PDF, CDR/transaction CSV, scanned image).
    Persists evidence metadata to DB and hashes the file for integrity.
    """
    # Verify Case exists
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    contents = await file.read()
    
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(contents).hexdigest()

    # Create Evidence ID
    count = db.query(Evidence).count()
    evidence_id = f"E-{count + 1:04d}"

    # Save to Secure Storage
    storage.save_file(evidence_id, contents)

    new_evidence = Evidence(
        id=evidence_id,
        case_id=case.id,
        file_name=file.filename,
        file_type=ext,
        source="Upload",
        sha256_hash=sha256_hash,
        integrity_status="unverified",
        provenance_status="registered"
    )
    db.add(new_evidence)
    
    # Record Provenance/Audit Log
    db_user = db.query(User).filter(User.username == user.username).first()
    audit_log = AuditLog(
        actor_id=db_user.id if db_user else None,
        role=user.role,
        action="UPLOADED",
        case_id=case.id,
        object_type="Evidence",
        object_id=evidence_id,
        reason=f"Uploaded file {file.filename} with hash {sha256_hash}"
    )
    db.add(audit_log)

    db.commit()
    db.refresh(new_evidence)

    return {
        "evidence_id": new_evidence.id,
        "case_id": new_evidence.case_id,
        "filename": new_evidence.file_name,
        "sha256": new_evidence.sha256_hash,
        "status": "queued_for_processing",
        "next_step": f"POST /api/process to run extraction pipeline on this document",
    }
