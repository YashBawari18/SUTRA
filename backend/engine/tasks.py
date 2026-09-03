from storage import storage
from engine.parsers import parse_document
from engine.entity_extraction import extract_entities_from_text
from engine.entity_resolution import resolve_entities
from database import SessionLocal, neo4j_conn
from models import Evidence, AuditLog
import datetime

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
        
        timestamp_now = datetime.datetime.utcnow().isoformat()
        
        # 4. Save to Neo4j (No silent merging - mark as pending_review)
        for ent in resolved_entities:
            query = f"""
            MERGE (n:`{ent['label']}` {{id: $id}})
            ON CREATE SET n.name = $name, n.case_id = $case_id, n.source = $source, 
                          n.verification_status = 'pending_review', n.evidence_id = $evidence_id
            ON MATCH SET n.name = $name
            """
            neo4j_session.run(query, id=ent['id'], name=ent['normalized_value'], case_id=evidence.case_id, source=ent['source'], evidence_id=evidence_id)
            
        for rel in relationships:
            rel_query = """
            MATCH (a {name: $source}), (b {name: $target})
            MERGE (a)-[r:RELATED_TO {type: $rel_type}]->(b)
            ON CREATE SET r.evidence_id = $evidence_id, r.confidence = $confidence, 
                          r.extraction_method = 'NLP Proximity', r.verification_status = 'pending_review',
                          r.timestamp = $timestamp
            """
            neo4j_session.run(rel_query, source=rel['source'].upper(), target=rel['target'].upper(), 
                              rel_type=rel['type'], evidence_id=evidence_id, confidence=rel.get('confidence', 0.5), timestamp=timestamp_now)

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

