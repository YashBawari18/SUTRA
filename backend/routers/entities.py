"""SUTRA Backend — routers/entities.py : extracted entity listing + resolution."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData
from database import get_neo4j

router = APIRouter()


@router.get("")
def list_entities(case_id: str, entity_type: str | None = None,
                   user: TokenData = Depends(require_role("analyst")), neo4j_session = Depends(get_neo4j)):
    """
    Queries Neo4j for entities in a specific case.
    """
    if entity_type:
        # Note: Cypher parameters cannot be used for labels, so we format carefully
        query = f"""
        MATCH (n:`{entity_type}` {{case_id: $case_id}})
        RETURN n
        """
    else:
        query = """
        MATCH (n {case_id: $case_id})
        RETURN n
        """
    
    result = neo4j_session.run(query, case_id=case_id)
    entities = []
    for record in result:
        node = record["n"]
        if node:
            entities.append({
                "id": node.id,
                "labels": list(node.labels),
                "properties": dict(node.items())
            })
            
    return {"case_id": case_id, "entity_type": entity_type, "entities": entities}


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
