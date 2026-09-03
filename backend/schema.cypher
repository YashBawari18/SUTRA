// SUTRA — Neo4j Graph Schema
// ============================
// Run these once against a fresh Neo4j instance (Neo4j Desktop, Aura,
// or `docker run neo4j`) to set up constraints and indexes before
// loading data.

// --- Uniqueness constraints (also creates an index automatically) ---
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT phone_id IF NOT EXISTS FOR (ph:Phone) REQUIRE ph.id IS UNIQUE;
CREATE CONSTRAINT vehicle_id IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT org_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT account_id IF NOT EXISTS FOR (a:BankAccount) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT case_id IF NOT EXISTS FOR (c:Case) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;

// --- Full-text search index for the AI assistant's entity lookup ---
CREATE FULLTEXT INDEX entityNameSearch IF NOT EXISTS
FOR (n:Person|Organization|Location) ON EACH [n.name];

// --- Example node creation (one per type — real data comes from the ingestion pipeline) ---
// MERGE (p:Person {id:"P01"}) SET p.name="Rajeev Malhotra", p.case_id="MH/CID/2026/0417";
// MERGE (ph:Phone {id:"PH01"}) SET ph.number="+91 98***1142";
// MERGE (p)-[:OWNS {source_record_id:"REC-001", confidence:0.95}]->(ph);

// --- Example relationship types used throughout the graph ---
// (:Person)-[:OWNS]->(:Phone|:Vehicle|:BankAccount)
// (:Person)-[:CALLED {weight:int, timestamp:datetime, suspicious:bool}]->(:Person)
// (:Person)-[:TRANSFERRED_MONEY {amount:float, timestamp:datetime}]->(:Person)
// (:Person)-[:VISITED {timestamp:datetime}]->(:Location)
// (:Person)-[:WORKS_FOR|:DIRECTOR_OF]->(:Organization)
// (:Person)-[:ASSOCIATED_WITH {confidence:float}]->(:Person)
// (:Organization)-[:LEASES]->(:Location)
// (:Entity)-[:MENTIONED_IN {source_reliability:string}]->(:Case)

// --- Example analytics queries (via Neo4j Graph Data Science library) ---
// Betweenness centrality:
// CALL gds.betweenness.stream('sutra-graph')
// YIELD nodeId, score
// RETURN gds.util.asNode(nodeId).name AS entity, score
// ORDER BY score DESC LIMIT 10;

// Community detection (Louvain):
// CALL gds.louvain.stream('sutra-graph')
// YIELD nodeId, communityId
// RETURN gds.util.asNode(nodeId).name AS entity, communityId;

// Shortest path between two entities:
// MATCH (a:Person {id:"P06"}), (b:Person {id:"P03"}),
//       path = shortestPath((a)-[*..6]-(b))
// RETURN path;
