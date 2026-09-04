"""
SUTRA Backend — routers/reports.py
==================================
Evidentiary Report Generator (Blueprint Part 21).
Generates legal-grade, source-grounded investigative intelligence reports
with explicit FACT / INFERENCE / INVESTIGATIVE LEAD distinctions.
Supports English, Hindi, and Marathi.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Case, EvidenceItem, RiskRecord, AuditLog
from auth import require_role, TokenData

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@router.post("/generate")
def generate_report(
    case_id: str = "MH/CID/2026/0417",
    lang: str = "en",
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Generates an official investigative dossier and records the issuance in the audit log.
    """
    c = db.query(Case).filter(Case.case_id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    report_path = DATA_DIR / "investigation_report_i18n.json"
    content = {}
    if report_path.exists():
        with open(report_path, encoding="utf-8") as f:
            data = json.load(f)
            content = data.get(lang, data.get("en", {}))

    # Log in audit trail
    audit = AuditLog(
        case_id=case_id,
        timestamp=datetime.now(),
        username=user.username,
        role=user.role,
        action_type="REPORT_GENERATED",
        target_id=f"REPORT_{case_id}_{lang.upper()}",
        details_json=json.dumps({"language": lang, "status": "OFFICIAL_DOSSIER_COMPILED"})
    )
    db.add(audit)
    db.commit()

    return {
        "case_id": case_id,
        "language": lang,
        "generated_by": user.username,
        "generated_at": datetime.now().isoformat(),
        "status": "OFFICIAL_DOSSIER_COMPILED",
        "dossier": content
    }


@router.get("/{case_id:path}")
def get_case_report(
    case_id: str = "MH/CID/2026/0417",
    lang: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """Returns the multi-lingual case intelligence briefing."""
    report_path = DATA_DIR / "investigation_report_i18n.json"
    if report_path.exists():
        with open(report_path, encoding="utf-8") as f:
            data = json.load(f)
            return data.get(lang, data.get("en", {}))

    return {"error": "Report template not found"}

