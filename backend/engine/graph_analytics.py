import networkx as nx

def calculate_graph_metrics(nodes, edges):
    """
    Computes NetworkX graph metrics for a given set of nodes and edges.
    nodes: list of dicts with 'id'
    edges: list of dicts with 'source' and 'target'
    Returns a dict mapping node_id to metrics.
    """
    G = nx.Graph()
    
    # Add nodes
    for node in nodes:
        G.add_node(node["id"], **node)
        
    # Add edges
    for edge in edges:
        G.add_edge(edge["source"], edge["target"])
        
    if len(G.nodes) == 0:
        return {}

    # Calculate metrics
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    try:
        pagerank = nx.pagerank(G)
    except Exception:
        pagerank = {n: 0 for n in G.nodes}
        
    # Community detection (Greedy Modularity - commonly referred to loosely as Louvain in some prototypes, but we will call it Modularity Communities)
    try:
        communities = nx.community.greedy_modularity_communities(G)
    except Exception:
        communities = []

    # Map communities to a dictionary for easy lookup
    community_map = {}
    for i, comm in enumerate(communities):
        for node_id in comm:
            community_map[node_id] = i

    results = {}
    for node_id in G.nodes:
        results[node_id] = {
            "degree_centrality": round(degree_cent.get(node_id, 0), 4),
            "betweenness_centrality": round(betweenness_cent.get(node_id, 0), 4),
            "pagerank": round(pagerank.get(node_id, 0), 4),
            "community_id": community_map.get(node_id, -1)
        }
        
    return results
