"""
SUTRA — Graph Construction & Analytics Engine
================================================
Builds a real NetworkX graph from the synthetic dataset and runs real
graph algorithms on it (blueprint Part 9): degree centrality,
betweenness centrality, PageRank, community detection, shortest paths.

This is the engine that would sit behind Neo4j in the production
architecture — same algorithms, same logic. NetworkX is used here
because it needs no server/install; a production build swaps the
storage layer, not the algorithms.

Run:  python3 graph_analytics.py
"""

import json
import os
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
with open(os.path.join(DATA_DIR, "dataset.json"), encoding="utf-8") as f:
    data = json.load(f)

G = nx.Graph()

# ---- Add nodes ----
def add_node(nid, label, ntype, **attrs):
    G.add_node(nid, label=label, type=ntype, **attrs)

for p in data["people"]:
    add_node(p["person_id"], p["name"], "person", notes=p.get("role_notes", ""))
for ph in data["phones"]:
    add_node(ph["phone_id"], ph["number"], "phone")
for v in data["vehicles"]:
    add_node(v["vehicle_id"], v["plate_number"], "vehicle")
for l in data["locations"]:
    add_node(l["location_id"], l["name"], "location")
for o in data["organizations"]:
    add_node(o["org_id"], o["name"], "organization", notes=o.get("notes", ""))
for a in data["accounts"]:
    add_node(a["account_id"], f"A/C {a['account_id']} ({a['bank']})", "account")

# ---- Ownership edges ----
for ph in data["phones"]:
    G.add_edge(ph["owner_person_id"], ph["phone_id"], type="OWNS", weight=1)
for v in data["vehicles"]:
    owner = v.get("owner_person_id") or v.get("owner_org_id")
    if owner:
        G.add_edge(owner, v["vehicle_id"], type="OWNS", weight=1)
for a in data["accounts"]:
    owner = a.get("holder_person_id") or a.get("holder_org_id")
    if owner:
        G.add_edge(owner, a["account_id"], type="OWNS", weight=1)
for o in data["organizations"]:
    if o.get("director_person_id"):
        G.add_edge(o["director_person_id"], o["org_id"], type="DIRECTOR_OF", weight=1)

# ---- Call edges (aggregated call count per phone pair) ----
call_counts = {}
for c in data["calls"]:
    key = tuple(sorted([c["caller_phone_id"], c["receiver_phone_id"]]))
    call_counts[key] = call_counts.get(key, 0) + 1

SUSPICIOUS_CALL_THRESHOLD = 15
for (a, b), n in call_counts.items():
    G.add_edge(a, b, type="CALLED", weight=n, suspicious=n >= SUSPICIOUS_CALL_THRESHOLD)

# ---- Visit edges (person/vehicle -> location) ----
for v in data["visits"]:
    loc = v["location_id"]
    if v.get("person_id"):
        G.add_edge(v["person_id"], loc, type="VISITED", weight=1, notes=v.get("notes", ""))
    elif v.get("vehicle_id"):
        G.add_edge(v["vehicle_id"], loc, type="VISITED", weight=1, notes=v.get("notes", ""))

# ---- Transaction edges (account -> account, flag large transfers) ----
LARGE_TXN_THRESHOLD = 500000
for t in data["transactions"]:
    G.add_edge(t["sender_account_id"], t["receiver_account_id"], type="TRANSFERRED_MONEY",
               weight=t["amount"], suspicious=t["amount"] >= LARGE_TXN_THRESHOLD,
               amount=t["amount"], timestamp=t["timestamp"])

print("Graph built:", G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")

# ------------------------------------------------------------------
# GRAPH ALGORITHMS
# ------------------------------------------------------------------
degree_c = nx.degree_centrality(G)
betweenness_c = nx.betweenness_centrality(G, weight=None)
pagerank = nx.pagerank(G, weight="weight")
components = list(nx.connected_components(G))
communities = list(greedy_modularity_communities(G))

# Rank "investigative priority entities" — persons/orgs only, per blueprint's
# instruction to never label them "criminal" — sorted by a blended score.
priority_candidates = [n for n, attrs in G.nodes(data=True) if attrs["type"] in ("person", "organization")]
priority_ranking = sorted(
    priority_candidates,
    key=lambda n: (0.5 * degree_c[n] + 0.3 * betweenness_c[n] + 0.2 * pagerank[n]),
    reverse=True
)

print("\nTOP INVESTIGATIVE-PRIORITY ENTITIES (by blended centrality — NOT an accusation):")
for n in priority_ranking[:5]:
    label = G.nodes[n]["label"]
    print(f"  {label:22s} degree={degree_c[n]:.3f}  betweenness={betweenness_c[n]:.3f}  pagerank={pagerank[n]:.3f}")

print(f"\nConnected components: {len(components)}")
print(f"Communities detected (Louvain-style greedy modularity): {len(communities)}")
for i, com in enumerate(communities):
    labels = [G.nodes[n]["label"] for n in com if G.nodes[n]["type"] == "person"]
    if labels:
        print(f"  Community {i+1}: {', '.join(labels)}")

# Example: shortest path between two entities that have NO direct link
# (this is the "hidden chain" reveal from the blueprint's demo case)
try:
    path = nx.shortest_path(G, source="P06", target="P03")  # Vikram -> ... -> Anita
    print("\nShortest path (Vikram Solanki -> Anita Rao):")
    print("  " + " -> ".join(G.nodes[n]["label"] for n in path))
except nx.NetworkXNoPath:
    print("\nNo path found between P06 and P03.")

# ------------------------------------------------------------------
# ROLE CLASSIFICATION & HIERARCHY
# ------------------------------------------------------------------
def classify_role(nid, attrs):
    ntype = attrs.get("type")
    if ntype != "person":
        return ntype.capitalize()
    
    bw = betweenness_c.get(nid, 0)
    pr = pagerank.get(nid, 0)
    deg = degree_c.get(nid, 0)
    
    # Financial involvement
    has_large_txn = False
    for t in data["transactions"]:
        if t.get("amount", 0) >= LARGE_TXN_THRESHOLD:
            # check account holder
            for a in data["accounts"]:
                if a.get("holder_person_id") == nid and (a["account_id"] in (t["sender_account_id"], t["receiver_account_id"])):
                    has_large_txn = True
                    break

    if bw >= 0.20:
        return "Strategic Broker"
    elif pr >= 0.025 and bw < 0.20:
        return "Network Orchestrator"
    elif has_large_txn:
        return "Financial Conduit"
    elif deg >= 0.10:
        return "Key Communicator"
    else:
        return "Network Associate"

# ------------------------------------------------------------------
# CHRONOLOGICAL EVENT TIMELINE COMPILATION
# ------------------------------------------------------------------
timeline_events = []
evt_id = 1

# 1. FIR events
for fir in data.get("fir_records", []):
    timeline_events.append({
        "id": f"evt_{evt_id}",
        "timestamp": f"{fir.get('date', '2026-02-14')} 09:00:00",
        "date": fir.get("date", "2026-02-14"),
        "time": "09:00",
        "type": "FIR_RECORD",
        "badge": "FIR FILED",
        "title": f"FIR Registered — {fir.get('case_id')} ({fir.get('station', 'Police Station')})",
        "description": fir.get("description", "")[:140] + "...",
        "nodes": [p["person_id"] for p in data["people"] if p["name"].split()[0].lower() in fir.get("description", "").lower()],
        "severity": "critical" if fir.get("source_reliability") == "High" else "warning"
    })
    evt_id += 1

# 2. Surveillance Visits
loc_map = {l["location_id"]: l["name"] for l in data.get("locations", [])}
person_map = {p["person_id"]: p["name"] for p in data.get("people", [])}
for v in data.get("visits", []):
    pid = v.get("person_id")
    pname = person_map.get(pid, "Identified Suspect")
    lname = loc_map.get(v.get("location_id"), "Observed Site")
    timeline_events.append({
        "id": f"evt_{evt_id}",
        "timestamp": v.get("timestamp", "2026-02-14 20:00:00"),
        "date": v.get("timestamp", "2026-02-14").split()[0],
        "time": v.get("timestamp", "2026-02-14 20:00").split()[1] if " " in v.get("timestamp", "") else "20:00",
        "type": "SURVEILLANCE",
        "badge": "SITE VISIT",
        "title": f"Surveillance Sighting — {pname}",
        "description": f"{pname} recorded at {lname}. Notes: {v.get('notes', 'Physical observation logged.')}",
        "nodes": [pid, v.get("location_id")] if pid else [v.get("location_id")],
        "severity": "warning" if "unusual" in v.get("notes", "").lower() or "late" in v.get("notes", "").lower() else "info"
    })
    evt_id += 1

# 3. High-Value Financial Transactions
account_holder_map = {a["account_id"]: a.get("holder_person_id") or a.get("holder_org_id") for a in data.get("accounts", [])}
for t in data.get("transactions", []):
    src_holder = account_holder_map.get(t["sender_account_id"], t["sender_account_id"])
    tgt_holder = account_holder_map.get(t["receiver_account_id"], t["receiver_account_id"])
    src_name = person_map.get(src_holder, src_holder)
    tgt_name = person_map.get(tgt_holder, tgt_holder)
    is_susp = t["amount"] >= LARGE_TXN_THRESHOLD
    timeline_events.append({
        "id": f"evt_{evt_id}",
        "timestamp": t.get("timestamp", "2026-02-15 14:00:00"),
        "date": t.get("timestamp", "2026-02-15").split()[0],
        "time": t.get("timestamp", "2026-02-15 14:00").split()[1] if " " in t.get("timestamp", "") else "14:00",
        "type": "FINANCIAL",
        "badge": "WIRE TRANSFER",
        "title": f"Financial Transfer: ₹{t['amount']:,}",
        "description": f"Transfer of ₹{t['amount']:,} from {src_name} ({t['sender_account_id']}) to {tgt_name} ({t['receiver_account_id']}).",
        "nodes": [t["sender_account_id"], t["receiver_account_id"], src_holder, tgt_holder],
        "severity": "critical" if is_susp else "info"
    })
    evt_id += 1

# 4. Clustered CDR Burst Calls
phone_owner = {ph["phone_id"]: ph.get("owner_person_id") for ph in data.get("phones", [])}
phone_number_map = {ph["phone_id"]: ph.get("number", "Unknown") for ph in data.get("phones", [])}
for (p1, p2), n in call_counts.items():
    if n >= SUSPICIOUS_CALL_THRESHOLD:
        pid1 = phone_owner.get(p1)
        pid2 = phone_owner.get(p2)
        n1 = person_map.get(pid1, phone_number_map.get(p1, p1))
        n2 = person_map.get(pid2, phone_number_map.get(p2, p2))
        timeline_events.append({
            "id": f"evt_{evt_id}",
            "timestamp": "2026-02-14 18:00:00",
            "date": "2026-02-14",
            "time": "18:00",
            "type": "COMMUNICATION",
            "badge": "CDR BURST",
            "title": f"High-Frequency CDR Surge ({n} calls)",
            "description": f"Concentrated exchange between {n1} ({phone_number_map.get(p1, p1)}) and {n2} ({phone_number_map.get(p2, p2)}) across 48h.",
            "nodes": [p1, p2, pid1, pid2],
            "severity": "critical"
        })
        evt_id += 1

timeline_events.sort(key=lambda x: x["timestamp"])

# ------------------------------------------------------------------
# ALL-PAIRS SHORTEST PATHS FOR INSTANT TRACE
# ------------------------------------------------------------------
all_paths = {}
for p_src in data["people"]:
    for p_tgt in data["people"]:
        if p_src["person_id"] != p_tgt["person_id"]:
            k = f"{p_src['person_id']}_{p_tgt['person_id']}"
            try:
                sp = nx.shortest_path(G, source=p_src["person_id"], target=p_tgt["person_id"])
                all_paths[k] = {
                    "path": sp,
                    "labels": [G.nodes[n]["label"] for n in sp],
                    "hops": len(sp) - 1
                }
            except nx.NetworkXNoPath:
                all_paths[k] = None

# ------------------------------------------------------------------
# EXPORT for the dashboard (nodes + edges + computed metrics)
# ------------------------------------------------------------------
export_nodes = []
for n, attrs in G.nodes(data=True):
    export_nodes.append({
        "id": n, "label": attrs["label"], "type": attrs["type"],
        "degree": round(degree_c[n], 4), "betweenness": round(betweenness_c[n], 4),
        "pagerank": round(pagerank[n], 4),
        "role": classify_role(n, attrs),
        "priority_rank": priority_ranking.index(n) + 1 if n in priority_ranking else None
    })

export_edges = []
for u, v, attrs in G.edges(data=True):
    edge = {"source": u, "target": v}
    edge.update(attrs)
    export_edges.append(edge)

export = {
    "nodes": export_nodes,
    "edges": export_edges,
    "communities": [[n for n in com] for com in communities],
    "priority_ranking": priority_ranking,
    "timeline_events": timeline_events,
    "all_paths": all_paths,
    "shortest_path_example": path if 'path' in dir() else None,
}
out_path = os.path.join(DATA_DIR, "graph_analytics_results.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(export, f, indent=2)
print(f"\nSaved graph + analytics + timeline events -> {out_path}")
