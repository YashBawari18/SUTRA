"""SUTRA Backend — routers/process.py : document processing pipeline."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from auth import require_role, TokenData
from database import get_db
from models import Evidence
from engine.tasks import process_evidence_task

router = APIRouter()

@router.post("/{evidence_id}")
async def trigger_processing(
    evidence_id: str,
    background_tasks: BackgroundTasks,
    user: TokenData = Depends(require_role("investigator")),
    db: Session = Depends(get_db)
):
    """
    Enqueues the extraction pipeline (parsing -> NLP) for a registered document.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    if evidence.provenance_status == "parsed":
        return {"status": "already_processed", "evidence_id": evidence_id}

    # Dispatch to background task
    background_tasks.add_task(process_evidence_task, evidence_id)
    
    return {
        "status": "processing_started",
        "evidence_id": evidence_id,
        "message": "Document queued for parsing and extraction pipeline."
    }
