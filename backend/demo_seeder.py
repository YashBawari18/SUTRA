import os
from database import SessionLocal, neo4j_conn
from models import Case, Evidence, User, RoleEnum

def seed_demo_data():
    db = SessionLocal()
    neo4j_session = neo4j_conn.get_session()
    
    print("Seeding Operation Phantom dataset...")
    
    try:
        # 1. Create Case in PostgreSQL
        case_id = "C-0992"
        demo_case = db.query(Case).filter(Case.id == case_id).first()
        if not demo_case:
            demo_case = Case(
                id=case_id,
                title="Operation Phantom (Hawala Syndicate)",
                description="Massive cross-border money laundering operation masking as logistics.",
                status="open",
                jurisdiction="Delhi HQ",
                sensitivity="restricted",
                created_by_id=1
            )
            db.add(demo_case)
            db.commit()

        # 2. Wipe existing Neo4j data for this case to avoid duplicates
        neo4j_session.run("MATCH (n {case_id: $case_id}) DETACH DELETE n", case_id=case_id)

        # 3. Create Graph Entities
        entities = [
            {"label": "Person", "id": "P-01", "name": "Rajeev Sharma", "risk_score": 92},
            {"label": "Person", "id": "P-02", "name": "Vikram Singh", "risk_score": 85},
            {"label": "Person", "id": "P-03", "name": "Amit Patel", "risk_score": 78},
            {"label": "Organization", "id": "O-01", "name": "Phantom Logistics Ltd", "risk_score": 95},
            {"label": "Organization", "id": "O-02", "name": "Global Exports Inc", "risk_score": 88},
            {"label": "Location", "id": "L-01", "name": "102 Cyber Park, Gurugram"},
            {"label": "Location", "id": "L-02", "name": "Port of Nhava Sheva"},
            {"label": "Phone", "id": "PH-01", "name": "+91-98765-43210"},
            {"label": "Phone", "id": "PH-02", "name": "+91-87654-32109"},
            {"label": "BankAccount", "id": "BA-01", "name": "HDFC-1092837465"}
        ]
        
        for ent in entities:
            query = f"""
            MERGE (n:`{ent['label']}` {{id: $id}})
            SET n.name = $name, n.case_id = $case_id, n.risk_score = $risk_score, n.verification_status = 'verified'
            """
            neo4j_session.run(query, id=ent['id'], name=ent['name'], case_id=case_id, risk_score=ent.get('risk_score', 0))

        # 4. Create Graph Relationships
        relationships = [
            ("P-01", "OWNS", "O-01", {"confidence": 0.95}),
            ("P-01", "COMMUNICATED_WITH", "P-02", {"confidence": 0.92, "frequency": 42}),
            ("P-02", "TRANSFERRED_FUNDS", "BA-01", {"confidence": 0.99, "amount": 5000000}),
            ("BA-01", "BELONGS_TO", "O-01", {"confidence": 1.0}),
            ("O-01", "REGISTERED_AT", "L-01", {"confidence": 1.0}),
            ("P-03", "VISITED", "L-01", {"confidence": 0.85}),
            ("P-03", "WORKS_FOR", "O-02", {"confidence": 0.90}),
            ("O-02", "SHIPS_VIA", "L-02", {"confidence": 0.88}),
            ("P-01", "USES_PHONE", "PH-01", {"confidence": 1.0}),
            ("P-02", "USES_PHONE", "PH-02", {"confidence": 0.95}),
            ("PH-01", "CALLED", "PH-02", {"confidence": 1.0, "duration": 1500})
        ]
        
        for source, rel_type, target, props in relationships:
            prop_str = ", ".join([f"{k}: ${k}" for k in props.keys()])
            if prop_str: prop_str = "{" + prop_str + "}"
            
            query = f"""
            MATCH (a {{id: $source}}), (b {{id: $target}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r += $props, r.verification_status = 'verified', r.case_id = $case_id
            """
            neo4j_session.run(query, source=source, target=target, props=props, case_id=case_id)
            
        print("Dataset seeded successfully! Ready for SIH presentation.")
    finally:
        db.close()
        neo4j_session.close()

if __name__ == "__main__":
    seed_demo_data()
