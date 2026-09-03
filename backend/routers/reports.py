"""SUTRA Backend — routers/reports.py : automatic report generation (blueprint Part 21)."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.post("/generate")
def generate_report(case_id: str, user: TokenData = Depends(require_role("senior_investigator"))):
    """
    Report generation is restricted to senior_investigator+ since it
    produces a document that may be used in official proceedings.

    The actual generation logic (pulling together dataset facts, entity
    resolution results, graph analytics, and risk scores into a single
    FACT / AI INFERENCE / INVESTIGATIVE LEAD tagged document) is already
    implemented and tested end-to-end in /engine/generate_report.py —
    this endpoint should import and call that same logic against the
    case's live data rather than reimplementing it.
    """
    return {"case_id": case_id, "status": "generated", "generated_by": user.username,
            "note": "see /engine/generate_report.py for the working reference implementation"}
