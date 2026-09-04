"""
SUTRA Backend — seed.py
=======================
Seeds the SQLite database with the complete investigative case:
Operation MH/CID/2026/0417 — Organised Financial & Smuggling Syndicate.

Populates:
  - Case metadata
  - Evidence Vault repository (with SHA-256 hashes, provenance chain, and custody)
  - Extracted Entities & Document graph nodes
  - Graph Relationships with explicit evidence ID links
  - Risk & Anomaly scoring breakdown records
  - Human Verification / Resolution candidates
  - Ingestion Pipeline history logs
  - Audit Trail
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from database import (
    init_db, SessionLocal, Case, EvidenceItem, Entity, Relationship,
    IngestionJob, ResolutionCandidate, RiskRecord, AuditLog
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def seed_database():
    init_db()
    db = SessionLocal()

    # Clear existing data for clean re-seed
    db.query(AuditLog).delete()
    db.query(RiskRecord).delete()
    db.query(ResolutionCandidate).delete()
    db.query(IngestionJob).delete()
    db.query(Relationship).delete()
    db.query(Entity).delete()
    db.query(EvidenceItem).delete()
    db.query(Case).delete()
    db.commit()

    case_id = "MH/CID/2026/0417"

    # 1. Create Case
    case = Case(
        case_id=case_id,
        title="Operation Red Thread — Hawala & Contraband Network",
        description="Multi-jurisdictional syndicate investigation involving illicit cross-border transfers, shell logistics companies, and burner cell communications operating across Mumbai, Thane, and Navi Mumbai.",
        status="active",
        created_by="Insp. Vikramaditya Kadam (CID Special Crime Unit)",
        created_at=datetime(2026, 2, 10, 8, 30)
    )
    db.add(case)

    # 2. Evidence Vault Items (with real SHA-256 integrity verification)
    fir_031_text = (
        "FIRST INFORMATION REPORT No. 031/2026\n"
        "Police Station: Andheri (East), Mumbai CID\n"
        "Date of Occurrence: 14/02/2026 at 21:30 hrs\n"
        "Complainant: Sub-Inspector S. Deshmukh (Surveillance Team 4)\n\n"
        "DETAILS: On 14/02/2026, surveillance team observed RAJEEV MALHOTRA (M/42) "
        "meeting FEROZ SHEIKH near the commercial warehouse at Andheri East. "
        "Vehicle bearing registration MH-04 GK 7729 was sighted departing at 22:45 hrs. "
        "Call records confirm SIM +91 98201 11422 made 18 calls to +91 77382 88341. "
        "Premises leased under SHREE TRADING CO. Complainant seized logistics consignment invoices."
    )
    fir_031_hash = hashlib.sha256(fir_031_text.encode("utf-8")).hexdigest()

    fir_014_text = (
        "LOCAL INTELLIGENCE REPORT No. 014/2026\n"
        "Police Station: Bhiwandi Town, Thane Rural\n"
        "Date: 26/01/2026\n"
        "Source: Field Informant 'Badger' (Unverified reliability rating: LOW)\n\n"
        "DETAILS: Informant reports SANJAY VERMA arranged cash lease for godown #4 in Bhiwandi "
        "approx 3 months prior. Multiple late-night cargo unloadings recorded without manifest. "
        "Associated commercial registration linked to Apex Logistics. Requires field confirmation."
    )
    fir_014_hash = hashlib.sha256(fir_014_text.encode("utf-8")).hexdigest()

    bank_text = (
        "CERTIFIED BANK STATEMENT & TRANSACTION LEDGER\n"
        "Issuer: State Bank of India & ICICI Special Compliance Unit\n"
        "Period: 01/01/2026 to 20/02/2026\n\n"
        "TXN-001: 2026-02-12 15:20:00 | A01 (Rajeev Malhotra) -> A02 (Anita Rao) | NEFT | INR 18,40,000 | Flagged Structuring\n"
        "TXN-002: 2026-01-18 11:05:00 | A03 (Vikram Solanki) -> A01 (Rajeev Malhotra) | IMPS | INR 2,50,000 | Clearing Fee\n"
        "TXN-003: 2026-01-22 09:40:00 | A04 (Shree Trading Co) -> A02 (Anita Rao) | UPI | INR 12,000 | Expense\n"
        "TXN-004: 2026-02-01 17:10:00 | A02 (Anita Rao) -> A01 (Rajeev Malhotra) | NEFT | INR 60,000 | Return credit"
    )
    bank_hash = hashlib.sha256(bank_text.encode("utf-8")).hexdigest()

    cdr_text = (
        "TELECOM SERVICE PROVIDER — CDR & BTS CELL TOWER DUMP\n"
        "Nodal Officer Mandate Ref: CID/CDR/2026/8991\n"
        "Coverage: Mumbai Metro Circle (Bandra, Andheri, BKC, Bhiwandi)\n\n"
        "1. +91 98201 11422 (Rajeev Malhotra) <-> +91 77382 88341 (Feroz Sheikh): 34 calls, 412 mins, 14 late-night\n"
        "2. +91 98201 11422 (Rajeev Malhotra) <-> +91 98201 55910 (Anita Rao): 28 calls, 194 mins, rapid burst prior to NEFT transfer\n"
        "3. +91 77382 88341 (Feroz Sheikh) <-> +91 91670 44211 (Vikram Solanki): 19 calls, 88 mins\n"
        "4. +91 98110 33901 (Sanjay Verma) <-> +91 91670 44211 (Vikram Solanki): 12 calls, 52 mins"
    )
    cdr_hash = hashlib.sha256(cdr_text.encode("utf-8")).hexdigest()

    surv_text = (
        "CID FIELD SURVEILLANCE LOG — OPERATION MH/CID/2026/0417\n"
        "Surveillance Unit: Delta-2 (Lead: Insp. Kadam)\n"
        "Date/Time: 14/02/2026 21:00 - 23:30 hrs\n\n"
        "21:15 - Subject Rajeev Malhotra arrived in silver Toyota Fortuner (MH-02 CR 1109).\n"
        "21:30 - Subject Feroz Sheikh arrived on foot from Western Express Highway side.\n"
        "21:35 - Handed over metallic briefcase inside warehouse gate 2.\n"
        "22:15 - Third subject identified via telephoto lens as Vikram Solanki arrived in vehicle MH-04 GK 7729.\n"
        "22:45 - All subjects departed. Physical photographs tagged under Exhibit SCU-09A through 09F."
    )
    surv_hash = hashlib.sha256(surv_text.encode("utf-8")).hexdigest()

    evidence_items = [
        EvidenceItem(
            evidence_id="EVID-2026-001",
            case_id=case_id,
            title="FIR No. 031/2026 — Andheri Warehouse Incident Report",
            source_type="FIR",
            source_agency="Maharashtra Police, Andheri PS",
            officer_name="Sub-Inspector S. Deshmukh",
            sha256_hash=fir_031_hash,
            file_path="data/fir_records.csv",
            content_text=fir_031_text,
            provenance_chain=json.dumps([
                {"timestamp": "2026-02-14T23:30:00", "actor": "SI Deshmukh", "action": "FIR Registered", "station": "Andheri PS"},
                {"timestamp": "2026-02-15T09:00:00", "actor": "Insp. V. Kadam", "action": "Transferred to CID Crime Vault", "station": "CID HQ"},
                {"timestamp": "2026-02-15T10:15:00", "actor": "SUTRA Ingestion System", "action": "Cryptographic Hash Registered", "hash": fir_031_hash}
            ]),
            reliability_score=0.92,
            verified_status="verified",
            verified_by="Insp. V. Kadam",
            verified_at=datetime(2026, 2, 15, 10, 30),
            created_at=datetime(2026, 2, 14, 23, 30)
        ),
        EvidenceItem(
            evidence_id="EVID-2026-002",
            case_id=case_id,
            title="Intelligence Report No. 014/2026 — Bhiwandi Warehouse Intel",
            source_type="FIELD_REPORT",
            source_agency="Thane Rural Special Branch",
            officer_name="Field Informant (ID: Badger)",
            sha256_hash=fir_014_hash,
            file_path="data/fir_records.csv",
            content_text=fir_014_text,
            provenance_chain=json.dumps([
                {"timestamp": "2026-01-26T14:00:00", "actor": "SB Field Agent", "action": "Human Source Debrief Logged", "station": "Bhiwandi"},
                {"timestamp": "2026-01-27T11:20:00", "actor": "SUTRA Ingestion System", "action": "Ingested with Unverified Flag", "hash": fir_014_hash}
            ]),
            reliability_score=0.45,
            verified_status="pending",
            verified_by="Awaiting Field Corroboration",
            verified_at=datetime(2026, 1, 27, 11, 20),
            created_at=datetime(2026, 1, 26, 14, 0)
        ),
        EvidenceItem(
            evidence_id="EVID-2026-003",
            case_id=case_id,
            title="Certified Bank Statement & Financial Transaction Ledger",
            source_type="BANK_RECORD",
            source_agency="State Bank of India & ICICI Special Compliance",
            officer_name="Chief Compliance Officer R. Mehta",
            sha256_hash=bank_hash,
            file_path="data/transactions.csv",
            content_text=bank_text,
            provenance_chain=json.dumps([
                {"timestamp": "2026-02-13T10:00:00", "actor": "SBI Compliance", "action": "STR (Suspicious Transaction Report) Filed", "station": "Fort Branch"},
                {"timestamp": "2026-02-13T16:45:00", "actor": "Insp. V. Kadam", "action": "Judicial Production Order Served", "station": "CID Economic Offences"},
                {"timestamp": "2026-02-13T18:00:00", "actor": "SUTRA Ingestion System", "action": "Bank API Sync & SHA-256 Certified", "hash": bank_hash}
            ]),
            reliability_score=0.98,
            verified_status="verified",
            verified_by="Insp. V. Kadam",
            verified_at=datetime(2026, 2, 13, 18, 30),
            created_at=datetime(2026, 2, 13, 16, 45)
        ),
        EvidenceItem(
            evidence_id="EVID-2026-004",
            case_id=case_id,
            title="Telecom Service Provider CDR & Tower Cell Dump",
            source_type="CDR",
            source_agency="Department of Telecom / Nodal Cell Mumbai",
            officer_name="Nodal Liaison Officer P. Sharma",
            sha256_hash=cdr_hash,
            file_path="data/calls.csv",
            content_text=cdr_text,
            provenance_chain=json.dumps([
                {"timestamp": "2026-02-15T08:00:00", "actor": "Nodal Officer", "action": "Lawful Interception Dump Extracted", "station": "DoT Mumbai"},
                {"timestamp": "2026-02-15T09:30:00", "actor": "SUTRA Ingestion System", "action": "CDR Analytics Parser Normalized 148 Records", "hash": cdr_hash}
            ]),
            reliability_score=0.95,
            verified_status="verified",
            verified_by="Analyst Priya Sen",
            verified_at=datetime(2026, 2, 15, 10, 0),
            created_at=datetime(2026, 2, 15, 8, 0)
        ),
        EvidenceItem(
            evidence_id="EVID-2026-005",
            case_id=case_id,
            title="CID Physical Surveillance Observation Report (Delta-2)",
            source_type="SURVEILLANCE",
            source_agency="CID Special Surveillance Unit, Delta-2",
            officer_name="Insp. Vikramaditya Kadam",
            sha256_hash=surv_hash,
            file_path="data/visits.csv",
            content_text=surv_text,
            provenance_chain=json.dumps([
                {"timestamp": "2026-02-14T23:45:00", "actor": "Surveillance Delta-2", "action": "Physical Observation Log Submitted", "station": "CID Mobile Unit"},
                {"timestamp": "2026-02-15T08:15:00", "actor": "SUTRA Ingestion System", "action": "Photographic & Geospatial Stamp Validated", "hash": surv_hash}
            ]),
            reliability_score=0.88,
            verified_status="verified",
            verified_by="Insp. V. Kadam",
            verified_at=datetime(2026, 2, 15, 8, 30),
            created_at=datetime(2026, 2, 14, 23, 45)
        )
    ]
    for ev in evidence_items:
        db.add(ev)

    # 3. Load Graph Nodes and Edges from graph_analytics_results.json
    graph_path = DATA_DIR / "graph_analytics_results.json"
    if graph_path.exists():
        with open(graph_path, encoding="utf-8") as f:
            graph_data = json.load(f)

        # Seed all 30 graph entities
        for node in graph_data.get("nodes", []):
            ent = Entity(
                entity_id=node["id"],
                case_id=case_id,
                label=node.get("label", node["id"]),
                type=node.get("type", "unknown"),
                role=node.get("role", "Associate"),
                aliases=json.dumps(node.get("aliases", [])),
                attributes_json=json.dumps({
                    "phone": node.get("phone"),
                    "account": node.get("account"),
                    "vehicle": node.get("vehicle"),
                    "reg": node.get("reg"),
                    "address": node.get("address"),
                    "degree": node.get("degree"),
                    "pagerank": node.get("pagerank"),
                    "community": node.get("community"),
                    "betweenness": node.get("betweenness")
                }),
                created_at=datetime(2026, 2, 15)
            )
            db.add(ent)

        # Add Document Graph Nodes (representing evidence directly on the graph)
        for ev in evidence_items:
            doc_ent = Entity(
                entity_id=f"DOC_{ev.evidence_id}",
                case_id=case_id,
                label=f"[{ev.source_type}] {ev.title[:22]}...",
                type="document",
                role="Legal Evidence Document",
                aliases=json.dumps([ev.evidence_id]),
                attributes_json=json.dumps({
                    "evidence_id": ev.evidence_id,
                    "source_agency": ev.source_agency,
                    "sha256": ev.sha256_hash[:16] + "...",
                    "reliability": ev.reliability_score,
                    "verified_status": ev.verified_status
                }),
                created_at=ev.created_at
            )
            db.add(doc_ent)

        # Seed all 34 graph edges
        for edge in graph_data.get("edges", []):
            # Determine backing evidence IDs
            ev_list = []
            rel_t = edge.get("type", "")
            if rel_t == "CALLED":
                ev_list = ["EVID-2026-004"]
            elif rel_t == "TRANSFERRED_MONEY":
                ev_list = ["EVID-2026-003"]
            elif rel_t == "VISITED":
                ev_list = ["EVID-2026-001", "EVID-2026-005"]
            elif rel_t in ("OWNS", "WORKS_FOR", "ASSOCIATED_WITH"):
                ev_list = ["EVID-2026-001"]
            else:
                ev_list = ["EVID-2026-001"]

            rel = Relationship(
                case_id=case_id,
                source_id=edge["source"],
                target_id=edge["target"],
                rel_type=rel_t,
                weight=edge.get("weight", 1),
                amount=edge.get("amount"),
                notes=edge.get("notes", ""),
                evidence_ids=json.dumps(ev_list),
                timestamp=edge.get("timestamp", "2026-02-14T21:30:00")
            )
            db.add(rel)

            # Connect Source Entity to Document Node for graph traceability
            for evid in ev_list:
                doc_edge = Relationship(
                    case_id=case_id,
                    source_id=edge["source"],
                    target_id=f"DOC_{evid}",
                    rel_type="CITED_IN_EVIDENCE",
                    weight=1,
                    amount=None,
                    notes=f"Corroborated by {evid}",
                    evidence_ids=json.dumps([evid]),
                    timestamp="2026-02-15T10:00:00"
                )
                db.add(doc_edge)


    # 4. Risk Records
    risk_path = DATA_DIR / "risk_scores.json"
    if risk_path.exists():
        with open(risk_path, encoding="utf-8") as f:
            risk_data = json.load(f)
            for r in risk_data:
                rr = RiskRecord(
                    case_id=case_id,
                    entity_id=r.get("person_id", r.get("name")),
                    name=r.get("name", "Unknown"),
                    risk_score=r.get("risk_indicator_score", 0),
                    breakdown_json=json.dumps(r.get("breakdown", {})),
                    factors_json=json.dumps(r.get("factors", {})),
                    calculated_at=datetime.utcnow()
                )
                db.add(rr)

    # 5. Entity Resolution Candidates (Requiring Human Verification)
    candidates = [
        ResolutionCandidate(
            case_id=case_id,
            source_mention="R. Malhotra (FIR-031)",
            target_mention="Rajeev Malhotra (P01)",
            suggested_entity_id="P01",
            similarity_score=0.88,
            confidence=0.91,
            shared_attributes=json.dumps(["Shared Phone: +91 98201 11422", "Location: Andheri East"]),
            status="pending"
        ),
        ResolutionCandidate(
            case_id=case_id,
            source_mention="Anita R. (HDFC Bank STR)",
            target_mention="Anita Rao (P02)",
            suggested_entity_id="P02",
            similarity_score=0.84,
            confidence=0.89,
            shared_attributes=json.dumps(["Shared Account A02", "Beneficiary of INR 18.4L transfer"]),
            status="pending"
        ),
        ResolutionCandidate(
            case_id=case_id,
            source_mention="Apex Logistics Fleet #7729",
            target_mention="MH-04 GK 7729 (Vehicle V02)",
            suggested_entity_id="V02",
            similarity_score=0.95,
            confidence=0.97,
            shared_attributes=json.dumps(["Identical Registration MH-04 GK 7729", "Registered to Sanjay Verma"]),
            status="approved",
            reviewed_by="Insp. V. Kadam",
            reviewed_at=datetime(2026, 2, 16, 11, 20)
        )
    ]
    for c in candidates:
        db.add(c)

    # 6. Ingestion Pipeline Jobs & Stage History
    ingestion_jobs = [
        IngestionJob(
            job_id="INGEST-JOB-2026-001",
            case_id=case_id,
            filename="FIR_Andheri_031_Scanned.pdf",
            file_type=".pdf",
            file_size=428190,
            sha256_hash=fir_031_hash,
            status="completed",
            current_stage="STAGE_6_INDEXED",
            stage_logs=json.dumps([
                {"stage": "1. Ingestion & Pre-processing", "status": "OK", "details": "MIME type PDF validated. SHA-256 generated."},
                {"stage": "2. OCR & Text Normalization", "status": "OK", "details": "Tesseract OCR extracted 1,240 tokens with 98.2% confidence."},
                {"stage": "3. Multilingual NLP Entity Extraction", "status": "OK", "details": "Extracted 4 Persons, 2 Phones, 1 Vehicle, 1 Org."},
                {"stage": "4. Entity Resolution & Dedup", "status": "OK", "details": "Matched Rajeev Malhotra (0.91 conf) with pending merge candidate."},
                {"stage": "5. Relationship & Temporal Linking", "status": "OK", "details": "Extracted 3 linkages (CALLED, VISITED, OWNS)."},
                {"stage": "6. Graph & Risk Indexing", "status": "OK", "details": "Graph centralities updated. Isolation Forest recalculated."}
            ]),
            extracted_counts=json.dumps({"entities": 8, "relationships": 3, "risk_delta": "+14%"}),
            evidence_id="EVID-2026-001",
            created_at=datetime(2026, 2, 15, 10, 15)
        ),
        IngestionJob(
            job_id="INGEST-JOB-2026-002",
            case_id=case_id,
            filename="CDR_Telecom_Circle_Bandra_Feb.csv",
            file_type=".csv",
            file_size=189400,
            sha256_hash=cdr_hash,
            status="completed",
            current_stage="STAGE_6_INDEXED",
            stage_logs=json.dumps([
                {"stage": "1. Ingestion & Pre-processing", "status": "OK", "details": "CSV delimiter detected. 148 CDR rows parsed."},
                {"stage": "2. OCR & Text Normalization", "status": "BYPASS", "details": "Digital structured CSV — OCR bypassed."},
                {"stage": "3. Multilingual NLP Entity Extraction", "status": "OK", "details": "Normalized 6 Phone numbers, 4 IMEI identifiers."},
                {"stage": "4. Entity Resolution & Dedup", "status": "OK", "details": "Phone numbers linked to registered subscriber entities."},
                {"stage": "5. Relationship & Temporal Linking", "status": "OK", "details": "Created 148 timestamped CALLED relationships."},
                {"stage": "6. Graph & Risk Indexing", "status": "OK", "details": "Communication burst detected (+38 calls in 48h)."}
            ]),
            extracted_counts=json.dumps({"entities": 10, "relationships": 8, "risk_delta": "+22%"}),
            evidence_id="EVID-2026-004",
            created_at=datetime(2026, 2, 15, 9, 30)
        ),
        IngestionJob(
            job_id="INGEST-JOB-2026-003",
            case_id=case_id,
            filename="Bank_STR_Mandate_NEFT_Logs.csv",
            file_type=".csv",
            file_size=84120,
            sha256_hash=bank_hash,
            status="completed",
            current_stage="STAGE_6_INDEXED",
            stage_logs=json.dumps([
                {"stage": "1. Ingestion & Pre-processing", "status": "OK", "details": "Certified banking XML/CSV structure verified."},
                {"stage": "2. OCR & Text Normalization", "status": "BYPASS", "details": "Direct API structured payload."},
                {"stage": "3. Multilingual NLP Entity Extraction", "status": "OK", "details": "4 Bank Accounts, 4 Currency Values Extracted."},
                {"stage": "4. Entity Resolution & Dedup", "status": "OK", "details": "Accounts mapped to P01, P02, P03, O01."},
                {"stage": "5. Relationship & Temporal Linking", "status": "OK", "details": "TRANSFERRED_MONEY links created with exact amounts."},
                {"stage": "6. Graph & Risk Indexing", "status": "OK", "details": "Financial anomaly score spiked for Anita Rao (INR 18.4L)."}
            ]),
            extracted_counts=json.dumps({"entities": 4, "relationships": 4, "risk_delta": "+35%"}),
            evidence_id="EVID-2026-003",
            created_at=datetime(2026, 2, 13, 18, 0)
        )
    ]
    for ij in ingestion_jobs:
        db.add(ij)

    # 7. Immutable Audit Trail
    audit_events = [
        AuditLog(
            case_id=case_id,
            timestamp=datetime(2026, 2, 10, 8, 30),
            username="Insp. V. Kadam",
            role="investigator",
            action_type="CASE_INITIATED",
            target_id=case_id,
            details_json=json.dumps({"rationale": "High Court writ petition mandate #7712 regarding Hawala smuggling"})
        ),
        AuditLog(
            case_id=case_id,
            timestamp=datetime(2026, 2, 13, 18, 30),
            username="Insp. V. Kadam",
            role="investigator",
            action_type="EVIDENCE_INTEGRITY_VERIFIED",
            target_id="EVID-2026-003",
            details_json=json.dumps({"hash": bank_hash, "source": "State Bank of India Compliance", "status": "MATCH_CONFIRMED"})
        ),
        AuditLog(
            case_id=case_id,
            timestamp=datetime(2026, 2, 15, 10, 30),
            username="Insp. V. Kadam",
            role="investigator",
            action_type="EVIDENCE_INTEGRITY_VERIFIED",
            target_id="EVID-2026-001",
            details_json=json.dumps({"hash": fir_031_hash, "source": "Andheri PS", "status": "MATCH_CONFIRMED"})
        ),
        AuditLog(
            case_id=case_id,
            timestamp=datetime(2026, 2, 16, 11, 20),
            username="Insp. V. Kadam",
            role="investigator",
            action_type="ENTITY_MERGE_APPROVED",
            target_id="V02",
            details_json=json.dumps({"merged_mention": "Apex Logistics Fleet #7729", "canonical_id": "V02", "confidence": 0.97})
        ),
        AuditLog(
            case_id=case_id,
            timestamp=datetime(2026, 2, 16, 14, 0),
            username="Analyst Priya Sen",
            role="analyst",
            action_type="SHORTEST_PATH_ANALYSIS",
            target_id="P01->P03",
            details_json=json.dumps({"source": "Rajeev Malhotra", "target": "Vikram Solanki", "hops": 3, "intermediary": "Feroz Sheikh"})
        )
    ]
    for ae in audit_events:
        db.add(ae)

    db.commit()
    db.close()
    print("Database successfully seeded with Operation MH/CID/2026/0417 data!")


if __name__ == "__main__":
    seed_database()
