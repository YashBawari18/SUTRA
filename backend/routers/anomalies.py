from fastapi import APIRouter, Depends, HTTPException
from auth import require_role, TokenData
from database import neo4j_conn
from engine.risk_scoring import compute_hybrid_risk
from engine.graph_analytics import calculate_graph_metrics

router = APIRouter()

@router.get("")
async def get_anomalies(
    case_id: str,
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Retrieves dynamic risk scores and anomalies for entities in a specific case.
    """
    neo4j_session = neo4j_conn.get_session()
    try:
        # Fetch basic graph structure for this case
        nodes_result = neo4j_session.run("MATCH (n {case_id: $case_id}) RETURN id(n) as id, n.name as name", case_id=case_id)
        edges_result = neo4j_session.run("MATCH (n {case_id: $case_id})-[r]->(m {case_id: $case_id}) RETURN id(n) as source, id(m) as target", case_id=case_id)
        
        nodes = [{"id": record["id"], "name": record["name"]} for record in nodes_result]
        edges = [{"source": record["source"], "target": record["target"]} for record in edges_result]
        
        if not nodes:
            return {"case_id": case_id, "anomalies": []}

        # Calculate graph metrics
        metrics = calculate_graph_metrics(nodes, edges)
        
        # Calculate hybrid risk for each node
        anomalies = []
        for node in nodes:
            node_id = node["id"]
            node_metrics = metrics.get(node_id, {})
            # Mocking ML/Rule inputs for the MVP output
            mock_ml = {"is_anomaly": True} if node_metrics.get("degree_centrality", 0) > 0.5 else {}
            mock_entity = {"communication_bursts": 4} if "Malhotra" in str(node.get("name", "")) else {}
            
            risk = compute_hybrid_risk(mock_entity, node_metrics, mock_ml)
            
            if risk["hybrid_risk_score"] > 30: # Only return somewhat suspicious items
                anomalies.append({
                    "entity_id": node_id,
                    "entity_name": node["name"],
                    "risk_profile": risk
                })
                
        return {"case_id": case_id, "anomalies": sorted(anomalies, key=lambda x: x["risk_profile"]["hybrid_risk_score"], reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        neo4j_session.close()

