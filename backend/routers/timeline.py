"""SUTRA Backend — routers/timeline.py : temporal correlation endpoints (blueprint Part 10)."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def get_timeline(case_id: str, entity_id: str | None = None,
                  user: TokenData = Depends(require_role("analyst"))):
    """
    Returns a chronologically ordered list of events (calls, transactions,
    visits, FIR filings) for a case, optionally filtered to one entity's
    activity. The frontend synchronizes this with the graph view: clicking
    a timeline event highlights the corresponding nodes/edges.

    Detection of "suspicious sequences" (e.g. a call, then a location
    visit, then a transaction, then an incident, all within a tight
    window) is a straightforward sort-and-scan over this same event list —
    flag any window where >=3 distinct event types cluster within
    N minutes of each other, e.g. 90 minutes.
    """
    return {"case_id": case_id, "entity_id": entity_id, "events": []}
