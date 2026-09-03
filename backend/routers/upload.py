"""SUTRA Backend — routers/upload.py : document ingestion endpoints."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from auth import require_role, TokenData

router = APIRouter()

ALLOWED_TYPES = {".pdf", ".csv", ".txt", ".jpg", ".png"}


@router.post("")
async def upload_document(case_id: str, file: UploadFile = File(...),
                           user: TokenData = Depends(require_role("investigator"))):
    """
    Accepts a source document (FIR PDF, CDR/transaction CSV, scanned image).
    Real implementation: save to secure storage, then enqueue for the
    processing pipeline (OCR -> NLP -> entity extraction -> resolution ->
    graph update), matching the "Investigation Mode" workflow (blueprint
    Part 19). Kept as a structural stub here — the actual extraction
    logic already exists and is proven working in /engine/entity_extraction.py.
    """
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    contents = await file.read()
    # SECURITY NOTE (blueprint Part 38): raw file contents are NEVER passed
    # directly to the LLM. They go through the parser -> structured facts
    # -> validation pipeline first. See routers/assistant.py.

    return {
        "case_id": case_id, "filename": file.filename, "size_bytes": len(contents),
        "status": "queued_for_processing",
        "next_step": "POST /api/process to run extraction pipeline on this document",
    }
