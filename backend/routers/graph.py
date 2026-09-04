"""
SUTRA Backend — routers/graph.py
================================
Dynamic Knowledge Graph & Analytics Engine.
Features:
  - Live node & edge retrieval with linked Evidence IDs
  - Document graph node toggle (visualizing evidence in graph)
  - 2-hop exploration workflow (ego graph extraction)
  - Observed Shortest Path with intermediary connection reasoning
  - Source-aware graph exploration & source reliability filtering
  - Live centrality, betweenness, PageRank, and community detection
"""

import json
from typing import Optional, List
import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, Entity, Relationship, EvidenceItem, AuditLog
from auth import require_role, TokenData

router = APIRouter()


def build_networkx_graph(db: Session, case_id: str, include_documents: bool = False):
    """Constructs a NetworkX MultiGraph from SQLite database."""
    G = nx.MultiGraph()

    q_nodes = db.query(Entity).filter(Entity.case_id == case_id)
    if not include_documents:
        q_nodes = q_nodes.filter(Entity.type != "document")

    nodes = q_nodes.all()
    for n in nodes:
        attrs = json.loads(n.attributes_json or "{}")
        G.add_node(
            n.entity_id,
            label=n.label,
            type=n.type,
            role=n.role,
            **attrs
        )

    q_edges = db.query(Relationship).filter(Relationship.case_id == case_id)
    if not include_documents:
        q_edges = q_edges.filter(Relationship.rel_type != "CITED_IN_EVIDENCE")

    edges = q_edges.all()
    for e in edges:
        if G.has_node(e.source_id) and G.has_node(e.target_id):
            ev_list = json.loads(e.evidence_ids or "[]")
            G.add_edge(
                e.source_id,
                e.target_id,
                key=e.id,
                rel_type=e.rel_type,
                weight=e.weight or 1,
                amount=e.amount,
                notes=e.notes,
                evidence_ids=ev_list,
                timestamp=e.timestamp
            )

    return G, nodes, edges


def compute_graph_payload(
    case_id: str,
    include_documents: bool,
    source_type: Optional[str],
    db: Session
):
    G, db_nodes, db_edges = build_networkx_graph(db, case_id, include_documents)

    if len(G.nodes) == 0:
        return {"case_id": case_id, "nodes": [], "edges": [], "summary": "No graph data"}

    # Compute network metrics
    simple_g = nx.Graph(G)
    degree_cent = nx.degree_centrality(simple_g)
    betweenness_cent = nx.betweenness_centrality(simple_g)
    try:
        pagerank_scores = nx.pagerank(simple_g, alpha=0.85)
    except Exception:
        pagerank_scores = {n: 0.01 for n in G.nodes}

    # Community detection
    try:
        from networkx.algorithms.community import louvain_communities
        communities = louvain_communities(simple_g)
        comm_map = {}
        for c_idx, comm in enumerate(communities):
            for node_id in comm:
                comm_map[node_id] = c_idx
    except Exception:
        comm_map = {n: 0 for n in G.nodes}

    # Filter by source type if requested
    allowed_evidence_ids = None
    if source_type:
        ev_records = db.query(EvidenceItem).filter(
            EvidenceItem.case_id == case_id,
            EvidenceItem.source_type == source_type.upper()
        ).all()
        allowed_evidence_ids = {e.evidence_id for e in ev_records}

    node_list = []
    for n in db_nodes:
        if not G.has_node(n.entity_id):
            continue
        attrs = json.loads(n.attributes_json or "{}")
        node_list.append({
            "id": n.entity_id,
            "label": n.label,
            "type": n.type,
            "role": n.role,
            "degree": round(degree_cent.get(n.entity_id, 0), 4),
            "betweenness": round(betweenness_cent.get(n.entity_id, 0), 4),
            "pagerank": round(pagerank_scores.get(n.entity_id, 0), 4),
            "community": comm_map.get(n.entity_id, 0),
            "attributes": attrs
        })

    edge_list = []
    for e in db_edges:
        if not (G.has_node(e.source_id) and G.has_node(e.target_id)):
            continue
        ev_list = json.loads(e.evidence_ids or "[]")

        if allowed_evidence_ids is not None:
            if not any(evid in allowed_evidence_ids for evid in ev_list):
                continue

        display_label = e.rel_type
        if e.rel_type == "CALLED":
            display_label = f"{e.weight} calls"
        elif e.rel_type == "TRANSFERRED_MONEY":
            amt_str = f"₹{int(e.amount):,}" if e.amount else "Amount"
            display_label = amt_str
        elif e.rel_type == "VISITED" and e.notes:
            display_label = e.notes

        edge_list.append({
            "id": e.id,
            "source": e.source_id,
            "target": e.target_id,
            "type": e.rel_type,
            "display_label": display_label,
            "weight": e.weight,
            "amount": e.amount,
            "notes": e.notes,
            "evidence_ids": ev_list,
            "timestamp": e.timestamp
        })

    return {
        "case_id": case_id,
        "nodes": node_list,
        "edges": edge_list,
        "metrics": {
            "node_count": len(node_list),
            "edge_count": len(edge_list),
            "communities_count": len(set(comm_map.values())),
            "document_nodes_included": include_documents
        }
    }


# SPECIFIC ROUTES FIRST (Before {case_id})
@router.get("/network/{entity_id}")
def get_entity_network(
    entity_id: str,
    hops: int = Query(2, ge=1, le=4),
    case_id: str = "MH/CID/2026/0417",
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    2-Hop Exploration Workflow:
    Extracts the local ego-network around a specific target entity up to N hops.
    Surfaces key direct associates and second-degree bridges.
    """
    G, db_nodes, db_edges = build_networkx_graph(db, case_id, include_documents=False)

    if not G.has_node(entity_id):
        match_id = None
        for n, data in G.nodes(data=True):
            if entity_id.lower() in data.get("label", "").lower() or entity_id.lower() in n.lower():
                match_id = n
                break
        if not match_id:
            raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found in graph")
        entity_id = match_id

    simple_g = nx.Graph(G)
    ego_g = nx.ego_graph(simple_g, entity_id, radius=hops)

    sub_nodes = []
    for n in ego_g.nodes():
        node_rec = db.query(Entity).filter(Entity.entity_id == n, Entity.case_id == case_id).first()
        if node_rec:
            sub_nodes.append({
                "id": node_rec.entity_id,
                "label": node_rec.label,
                "type": node_rec.type,
                "role": node_rec.role,
                "distance_hops": nx.shortest_path_length(ego_g, source=entity_id, target=n)
            })

    sub_edges = []
    q_edges = db.query(Relationship).filter(Relationship.case_id == case_id).all()
    for e in q_edges:
        if ego_g.has_node(e.source_id) and ego_g.has_node(e.target_id):
            sub_edges.append({
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.rel_type,
                "weight": e.weight,
                "amount": e.amount,
                "evidence_ids": json.loads(e.evidence_ids or "[]")
            })

    return {
        "case_id": case_id,
        "center_entity_id": entity_id,
        "center_label": G.nodes[entity_id].get("label", entity_id),
        "hops": hops,
        "subgraph_nodes": sub_nodes,
        "subgraph_edges": sub_edges,
        "total_associates_discovered": len(sub_nodes) - 1
    }


@router.get("/path/shortest")
def find_shortest_path(
    source_id: str,
    target_id: str,
    case_id: str = "MH/CID/2026/0417",
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("investigator"))
):
    """
    Observed Shortest Path:
    Discovers the shortest evidentiary chain between any two entities in the network.
    Returns path nodes, intermediary relationships, backing evidence IDs, and risk interpretation.
    """
    G, db_nodes, db_edges = build_networkx_graph(db, case_id, include_documents=False)

    def resolve_node(query: str):
        if G.has_node(query):
            return query
        for n, data in G.nodes(data=True):
            if query.lower() in data.get("label", "").lower() or query.lower() in n.lower():
                return n
        return None

    src = resolve_node(source_id)
    tgt = resolve_node(target_id)

    if not src:
        raise HTTPException(status_code=404, detail=f"Source entity '{source_id}' not found")
    if not tgt:
        raise HTTPException(status_code=404, detail=f"Target entity '{target_id}' not found")

    simple_g = nx.Graph(G)
    try:
        path_nodes = nx.shortest_path(simple_g, source=src, target=tgt)
    except nx.NetworkXNoPath:
        return {
            "case_id": case_id,
            "source_id": src,
            "target_id": tgt,
            "path_exists": False,
            "message": "No observed path connecting these two entities in the current evidence graph."
        }

    steps = []
    path_evidence = set()
    for i in range(len(path_nodes) - 1):
        u, v = path_nodes[i], path_nodes[i+1]
        u_rec = db.query(Entity).filter(Entity.entity_id == u).first()
        v_rec = db.query(Entity).filter(Entity.entity_id == v).first()

        edge_rec = db.query(Relationship).filter(
            Relationship.case_id == case_id,
            ((Relationship.source_id == u) & (Relationship.target_id == v)) |
            ((Relationship.source_id == v) & (Relationship.target_id == u))
        ).first()

        ev_list = json.loads(edge_rec.evidence_ids or "[]") if edge_rec else []
        for ev in ev_list:
            path_evidence.add(ev)

        steps.append({
            "step_number": i + 1,
            "from_entity": {"id": u, "label": u_rec.label if u_rec else u, "type": u_rec.type if u_rec else ""},
            "to_entity": {"id": v, "label": v_rec.label if v_rec else v, "type": v_rec.type if v_rec else ""},
            "relationship": edge_rec.rel_type if edge_rec else "CONNECTED_TO",
            "details": edge_rec.notes if edge_rec else "",
            "amount": edge_rec.amount if edge_rec else None,
            "weight": edge_rec.weight if edge_rec else 1,
            "evidence_ids": ev_list
        })

    intermediaries = [G.nodes[n].get("label", n) for n in path_nodes[1:-1]]
    if intermediaries:
        reasoning = f"Connection established via {len(intermediaries)} intermediary bridge(s): {', '.join(intermediaries)}."
    else:
        reasoning = "Direct relationship exists between entities."

    return {
        "case_id": case_id,
        "source_id": src,
        "source_label": G.nodes[src].get("label", src),
        "target_id": tgt,
        "target_label": G.nodes[tgt].get("label", tgt),
        "path_exists": True,
        "total_hops": len(path_nodes) - 1,
        "path_nodes": path_nodes,
        "path_steps": steps,
        "backing_evidence_ids": list(path_evidence),
        "reasoning": reasoning,
        "requires_human_verification": True
    }


# GENERAL GRAPH ROUTE
@router.get("")
def get_graph_by_query(
    case_id: str = "MH/CID/2026/0417",
    include_documents: bool = False,
    source_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    return compute_graph_payload(case_id, include_documents, source_type, db)


@router.get("/{case_id:path}")
def get_graph(
    case_id: str,
    include_documents: bool = False,
    source_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    return compute_graph_payload(case_id, include_documents, source_type, db)
