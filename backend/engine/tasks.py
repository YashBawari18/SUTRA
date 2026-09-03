from storage import storage
from engine.parsers import parse_document
from engine.entity_extraction import extract_entities_from_text
from engine.entity_resolution import resolve_entities
from database import SessionLocal, neo4j_conn
from models import Evidence, AuditLog

def process_evidence_task(evidence_id: str):
    """
    Background task to parse raw text and run NLP extraction.
    """
    db = SessionLocal()
    neo4j_session = neo4j_conn.get_session()
    try:
        evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
        if not evidence:
            print(f"Task failed: Evidence {evidence_id} not found.")
            return

        # 1. Retrieve & Parse
        file_bytes = storage.get_file(evidence_id)
        raw_text = parse_document(evidence.file_type, file_bytes)
        
        # 2. Extract Entities (NLP & Regex)
        raw_entities, relationships = extract_entities_from_text(raw_text)
        
        # 3. Resolve & Normalize Entities
        resolved_entities = resolve_entities(raw_entities)
        
        # 4. Save to Neo4j
        for ent in resolved_entities:
            query = f"""
            MERGE (n:`{ent['label']}` {{id: $id}})
            ON CREATE SET n.name = $name, n.case_id = $case_id, n.source = $source
            ON MATCH SET n.name = $name
            """
            neo4j_session.run(query, id=ent['id'], name=ent['normalized_value'], case_id=evidence.case_id, source=ent['source'])
            
        for rel in relationships:
            # We must map raw source/target to resolved IDs. For simplicity in demo, we match by name.
            rel_query = """
            MATCH (a {name: $source}), (b {name: $target})
            MERGE (a)-[r:RELATED_TO {type: $rel_type}]->(b)
            """
            # Note: A real system uses resolved IDs here.
            neo4j_session.run(rel_query, source=rel['source'].upper(), target=rel['target'].upper(), rel_type=rel['type'])

        # 5. Update Status
        evidence.provenance_status = "extracted"
        audit_log = AuditLog(
            action="EXTRACTED",
            case_id=evidence.case_id,
            object_type="Evidence",
            object_id=evidence_id,
            reason=f"Extracted {len(resolved_entities)} entities."
        )
        db.add(audit_log)
        db.commit()
        
        print(f"Extraction complete for {evidence.file_name}.")
    except Exception as e:
        print(f"Task failed for {evidence_id}: {e}")
        db.rollback()
    finally:
        db.close()
        neo4j_session.close()

