"""SUTRA Backend — routers/graph.py : knowledge graph + analytics endpoints."""
from fastapi import APIRouter, Depends
from auth import require_role, TokenData

router = APIRouter()


@router.get("/{case_id}")
def get_graph(case_id: str, user: TokenData = Depends(require_role("analyst"))):
    """
    Production implementation runs a Cypher query against Neo4j to pull
    all nodes/edges for this case, e.g.:
        MATCH (n {case_id: $case_id})-[r]-(m {case_id: $case_id})
        RETURN n, r, m

    For the analytics values (degree/betweenness/PageRank/communities),
    call the Neo4j Graph Data Science library, OR reuse the already-working
    NetworkX implementation in /engine/graph_analytics.py directly if GDS
    is not licensed/available in your deployment.
    """
    return {"case_id": case_id, "nodes": [], "edges": [], "note": "wire to Neo4j or /engine/graph_analytics.py"}


@router.get("/network/{entity_id}")
def get_entity_network(entity_id: str, hops: int = 2,
                        user: TokenData = Depends(require_role("analyst"))):
    """Neo4j variable-length path query:
        MATCH path = (n {id:$entity_id})-[*1..$hops]-(m)
        RETURN path
    """
    return {"entity_id": entity_id, "hops": hops, "network": []}


@router.get("/shortest-path")
def shortest_path(source_id: str, target_id: str,
                   user: TokenData = Depends(require_role("investigator"))):
    """Neo4j: MATCH p = shortestPath((a {id:$source_id})-[*..8]-(b {id:$target_id})) RETURN p
    Already demonstrated working (NetworkX) in /engine/graph_analytics.py,
    which found: Vikram Solanki -> Phone -> Phone -> Anita Rao in the demo case."""
    return {"source_id": source_id, "target_id": target_id, "path": []}
