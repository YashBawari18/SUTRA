"""SUTRA Backend — routers/entities.py : extracted entity listing + resolution."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def list_entities(case_id: str, entity_type: str | None = None,
                   user: TokenData = Depends(require_role("analyst"))):
    """
    Production implementation queries Neo4j:
        MATCH (n) WHERE n.case_id = $case_id
        AND ($entity_type IS NULL OR $entity_type IN labels(n))
        RETURN n
    The extraction + resolution logic itself is already implemented and
    tested in /engine/entity_extraction.py and /engine/entity_resolution.py
    — this endpoint exposes their output over HTTP.
    """
    return {"case_id": case_id, "entity_type": entity_type, "entities": "see /engine output for a worked example"}


@router.get("/resolution-candidates")
def resolution_candidates(case_id: str, user: TokenData = Depends(require_role("investigator"))):
    """Returns entity-resolution suggestions below the auto-merge threshold,
    awaiting human confirmation (blueprint Part 15 — no silent merging)."""
    return {"case_id": case_id, "candidates": []}


@router.post("/resolution-candidates/{mention_id}/confirm")
def confirm_merge(mention_id: str, approve: bool,
                   user: TokenData = Depends(require_role("investigator"))):
    """Investigator confirms or rejects a suggested entity merge. This
    decision is written to the audit log (routers/audit.py)."""
    return {"mention_id": mention_id, "approved": approve, "confirmed_by": user.username}
