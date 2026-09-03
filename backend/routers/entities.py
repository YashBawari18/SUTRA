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
def resolution_candidates(case_id: str, user: TokenData = Depends(require_role("investigator")), neo4j_session = Depends(get_neo4j)):
    """Returns entity-resolution suggestions below the auto-merge threshold,
    awaiting human confirmation (blueprint Part 15 — no silent merging)."""
    
    query = """
    MATCH (n {case_id: $case_id, verification_status: 'pending_review'})
    RETURN n.id AS mention_id, n.name AS name, labels(n)[0] AS type
    LIMIT 10
    """
    results = neo4j_session.run(query, case_id=case_id)
    candidates = [{"mention_id": r["mention_id"], "name": r["name"], "type": r["type"]} for r in results]
    
    return {"case_id": case_id, "candidates": candidates}


from database import SessionLocal
from models import AuditLog, User

@router.post("/resolution-candidates/{mention_id}/confirm")
def confirm_merge(mention_id: str, approve: bool, case_id: str,
                   user: TokenData = Depends(require_role("investigator")), neo4j_session = Depends(get_neo4j)):
    """Investigator confirms or rejects a suggested entity merge. This
    decision is written to the audit log (routers/audit.py)."""
    
    new_status = 'verified' if approve else 'rejected'
    
    query = """
    MATCH (n {id: $mention_id})
    SET n.verification_status = $new_status
    """
    neo4j_session.run(query, mention_id=mention_id, new_status=new_status)
    
    db = SessionLocal()
    try:
        actor = db.query(User).filter(User.username == user.username).first()
        actor_id = actor.id if actor else None
        
        audit = AuditLog(
            actor_id=actor_id,
            role=user.role,
            action="VERIFIED" if approve else "REJECTED",
            case_id=case_id,
            object_type="Entity",
            object_id=mention_id,
            reason=f"Human investigator {'approved' if approve else 'rejected'} entity extraction."
        )
        db.add(audit)
        db.commit()
    finally:
        db.close()
        
    return {"mention_id": mention_id, "approved": approve, "status": new_status, "confirmed_by": user.username}

