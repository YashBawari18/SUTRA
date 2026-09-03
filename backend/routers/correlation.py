from fastapi import APIRouter, Depends
from auth import require_role, TokenData
from database import neo4j_conn

router = APIRouter()

@router.get("")
def get_correlations(case_id: str | None = None, user: TokenData = Depends(require_role("investigator"))):
    """
    Finds entities that overlap across multiple distinct evidence documents.
    Solves PRD Gap #22 (Cross-Source Correlation).
    """
    neo4j_session = neo4j_conn.get_session()
    
    query = """
    MATCH (n)-[:MENTIONED_IN]->(d1:Document), (n)-[:MENTIONED_IN]->(d2:Document)
    WHERE d1.id < d2.id
    """
    if case_id:
        query += " AND d1.case_id = $case_id AND d2.case_id = $case_id "
        
    query += """
    RETURN n.name AS entity, labels(n)[0] AS type, d1.filename AS source_1, d2.filename AS source_2
    LIMIT 50
    """
    
    try:
        results = neo4j_session.run(query, case_id=case_id)
        correlations = []
        for record in results:
            correlations.append({
                "entity": record["entity"],
                "type": record["type"],
                "sources": [record["source_1"], record["source_2"]]
            })
        return {"case_id": case_id, "correlations": correlations}
    finally:
        neo4j_session.close()
