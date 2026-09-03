"""SUTRA Backend — routers/graph.py : knowledge graph + analytics endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from auth import require_role, TokenData
from database import get_neo4j

router = APIRouter()

@router.get("/{case_id}")
def get_graph(case_id: str, user: TokenData = Depends(require_role("analyst")), neo4j_session = Depends(get_neo4j)):
    """
    Pulls all nodes and edges for this case from Neo4j.
    """
    query = """
    MATCH (n {case_id: $case_id})
    OPTIONAL MATCH (n)-[r]->(m {case_id: $case_id})
    RETURN n, r, m
    """
    result = neo4j_session.run(query, case_id=case_id)
    nodes = set()
    edges = []
    
    for record in result:
        node_n = record["n"]
        if node_n:
            nodes.add((node_n.id, frozenset(node_n.items()), frozenset(node_n.labels)))
        
        rel_r = record["r"]
        node_m = record["m"]
        if rel_r and node_m:
            nodes.add((node_m.id, frozenset(node_m.items()), frozenset(node_m.labels)))
            edges.append({
                "id": rel_r.id,
                "source": rel_r.start_node.id,
                "target": rel_r.end_node.id,
                "type": rel_r.type,
                "properties": dict(rel_r.items())
            })
            
    formatted_nodes = [
        {"id": n[0], "labels": list(n[2]), "properties": dict(n[1])}
        for n in nodes
    ]

    return {"case_id": case_id, "nodes": formatted_nodes, "edges": edges}

@router.get("/network/{entity_id}")
def get_entity_network(entity_id: str, hops: int = 2, user: TokenData = Depends(require_role("analyst")), neo4j_session = Depends(get_neo4j)):
    """Variable-length path query for a specific entity."""
    query = """
    MATCH path = (n {id: $entity_id})-[*1..$hops]-(m)
    RETURN path
    """
    # Note: Dynamic path length requires formatting, but Neo4j allows passing hops if stringified safely or explicitly set
    query = query.replace("$hops", str(int(hops)))
    
    result = neo4j_session.run(query, entity_id=entity_id)
    paths = []
    for record in result:
        # Simplify path serialization
        path = record["path"]
        paths.append([node.id for node in path.nodes])
        
    return {"entity_id": entity_id, "hops": hops, "network": paths}

@router.get("/shortest-path")
def shortest_path(source_id: str, target_id: str, user: TokenData = Depends(require_role("investigator")), neo4j_session = Depends(get_neo4j)):
    """Shortest path calculation between two entities."""
    query = """
    MATCH p = shortestPath((a {id: $source_id})-[*..8]-(b {id: $target_id}))
    RETURN p
    """
    result = neo4j_session.run(query, source_id=source_id, target_id=target_id)
    record = result.single()
    
    path_nodes = []
    if record and record["p"]:
        path_nodes = [node.id for node in record["p"].nodes]
        
    return {"source_id": source_id, "target_id": target_id, "path": path_nodes}
