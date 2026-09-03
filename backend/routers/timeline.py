from fastapi import APIRouter, Depends, HTTPException
from auth import require_role, TokenData
from database import neo4j_conn

router = APIRouter()

@router.get("")
async def get_timeline(case_id: str, entity_id: str | None = None,
                  user: TokenData = Depends(require_role("investigator"))):
    """
    Returns a chronologically ordered list of events derived from the graph.
    """
    neo4j_session = neo4j_conn.get_session()
    try:
        # Fetch relationships with timestamps
        query = """
        MATCH (a {case_id: $case_id})-[r]->(b {case_id: $case_id})
        WHERE r.timestamp IS NOT NULL
        """
        if entity_id:
            query = """
            MATCH (a {case_id: $case_id, id: $entity_id})-[r]->(b {case_id: $case_id})
            WHERE r.timestamp IS NOT NULL
            """
            
        query += " RETURN a.name AS source, b.name AS target, type(r) AS type, r.timestamp AS timestamp, r.evidence_id AS evidence ORDER BY r.timestamp ASC"
        
        result = neo4j_session.run(query, case_id=case_id, entity_id=entity_id)
        
        events = []
        for record in result:
            events.append({
                "timestamp": record["timestamp"],
                "event_type": record["type"],
                "description": f"{record['source']} {record['type']} {record['target']}",
                "evidence_id": record.get("evidence", "Unknown")
            })
            
        return {"case_id": case_id, "entity_id": entity_id, "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        neo4j_session.close()

