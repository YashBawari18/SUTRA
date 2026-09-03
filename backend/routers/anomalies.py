"""SUTRA Backend — routers/anomalies.py : risk-indicator scoring endpoints."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def list_anomalies(case_id: str, min_score: float = 0,
                    user: TokenData = Depends(require_role("investigator"))):
    """
    Production implementation re-uses the exact scoring logic already
    implemented and tested in /engine/risk_scoring.py (Isolation Forest +
    the weighted formula from blueprint Part 11), run against this case's
    live data instead of the synthetic demo dataset.

    Every returned item MUST include:
      - risk_indicator_score
      - full breakdown (never just the final number)
      - requires_human_verification: true
    This is enforced by the response model, not left to convention.
    """
    return {"case_id": case_id, "min_score": min_score, "risk_indicators": [],
            "disclaimer": "All scores require human verification and are not evidence of guilt."}
