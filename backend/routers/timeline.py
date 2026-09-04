"""
SUTRA Backend — routers/timeline.py
===================================
Dedicated Investigation Timeline Engine.
Delivers:
  - Chronological multi-source event stream (Calls, Transactions, Surveillance, FIRs)
  - Timeline filtering by entity and event type
  - Cross-source evidence correlation
  - Timeline-linked risk indicators
  - Relationship history between pairs of entities over time
"""

import json
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Relationship, Entity, EvidenceItem
from auth import require_role, TokenData

router = APIRouter()

# Canonical investigative events for Operation MH/CID/2026/0417
BASE_EVENTS = [
    {
        "id": "EVT-001",
        "timestamp": "2026-01-15T10:00:00",
        "date_formatted": "15 Jan 2026",
        "time_formatted": "10:00 AM",
        "type": "SURVEILLANCE",
        "badge": "SITE VISIT",
        "title": "Surveillance Sighting — Anita Rao",
        "description": "Anita Rao observed at Nariman Point corporate office. Registered workplace.",
        "entities": ["P02", "L03"],
        "severity": "info",
        "evidence_id": "EVID-2026-005",
        "is_risk_spike": False
    },
    {
        "id": "EVT-002",
        "timestamp": "2026-01-18T11:05:00",
        "date_formatted": "18 Jan 2026",
        "time_formatted": "11:05 AM",
        "type": "TRANSACTION",
        "badge": "IMPS TRANSFER",
        "title": "Bank Transfer: ₹2,50,000 to Rajeev Malhotra",
        "description": "Account A03 (Vikram Solanki) initiated IMPS transfer to A01 (Rajeev Malhotra). Flagged clearing fee.",
        "entities": ["P03", "P01", "A03", "A01"],
        "severity": "warn",
        "evidence_id": "EVID-2026-003",
        "is_risk_spike": True
    },
    {
        "id": "EVT-003",
        "timestamp": "2026-01-22T09:40:00",
        "date_formatted": "22 Jan 2026",
        "time_formatted": "09:40 AM",
        "type": "TRANSACTION",
        "badge": "UPI TRANSFER",
        "title": "UPI Payment: ₹12,000 to Anita Rao",
        "description": "Account A04 (Shree Trading Co.) transferred ₹12,000 via UPI to A02 (Anita Rao). Operational petty expense.",
        "entities": ["O01", "P02", "A04", "A02"],
        "severity": "info",
        "evidence_id": "EVID-2026-003",
        "is_risk_spike": False
    },
    {
        "id": "EVT-004",
        "timestamp": "2026-01-26T14:00:00",
        "date_formatted": "26 Jan 2026",
        "time_formatted": "02:00 PM",
        "type": "FIR",
        "badge": "INTEL REPORT",
        "title": "Bhiwandi Godown Informant Report Logged",
        "description": "Local intelligence report No. 014/2026 logged at PS Bhiwandi. Sanjay Verma leased godown under unverified cash deal.",
        "entities": ["P05", "L02"],
        "severity": "warn",
        "evidence_id": "EVID-2026-002",
        "is_risk_spike": False
    },
    {
        "id": "EVT-005",
        "timestamp": "2026-02-01T17:10:00",
        "date_formatted": "01 Feb 2026",
        "time_formatted": "05:10 PM",
        "type": "TRANSACTION",
        "badge": "NEFT TRANSFER",
        "title": "NEFT Remittance: ₹60,000 to Rajeev Malhotra",
        "description": "Account A02 (Anita Rao) remitted ₹60,000 back to A01 (Rajeev Malhotra).",
        "entities": ["P02", "P01", "A02", "A01"],
        "severity": "info",
        "evidence_id": "EVID-2026-003",
        "is_risk_spike": False
    },
    {
        "id": "EVT-006",
        "timestamp": "2026-02-10T08:30:00",
        "date_formatted": "10 Feb 2026",
        "time_formatted": "08:30 AM",
        "type": "FIR",
        "badge": "CASE INITIATION",
        "title": "Formal CID Investigation Registered",
        "description": "Operation MH/CID/2026/0417 formally initiated under High Court mandate by Insp. Vikramaditya Kadam.",
        "entities": ["P01", "P02", "P03", "P04", "P05"],
        "severity": "info",
        "evidence_id": "EVID-2026-001",
        "is_risk_spike": False
    },
    {
        "id": "EVT-007",
        "timestamp": "2026-02-12T15:20:00",
        "date_formatted": "12 Feb 2026",
        "time_formatted": "03:20 PM",
        "type": "TRANSACTION",
        "badge": "CRITICAL ANOMALY",
        "title": "High-Value Transfer: ₹18,40,000 to Anita Rao",
        "description": "Major Hawala structuring detected: Account A01 (Rajeev Malhotra) to A02 (Anita Rao). Financial anomaly z-score spiked to 98.4.",
        "entities": ["P01", "P02", "A01", "A02"],
        "severity": "crit",
        "evidence_id": "EVID-2026-003",
        "is_risk_spike": True
    },
    {
        "id": "EVT-008",
        "timestamp": "2026-02-13T10:00:00",
        "date_formatted": "13 Feb 2026",
        "time_formatted": "10:00 AM",
        "type": "CALL",
        "badge": "CDR BURST",
        "title": "Communication Spike: 14 Calls in 4 Hours",
        "description": "Rapid frequency calls between +91 98201 11422 (Malhotra) and +91 77382 88341 (Feroz Sheikh). Precursor to physical meeting.",
        "entities": ["P01", "P04", "PH01", "PH04"],
        "severity": "crit",
        "evidence_id": "EVID-2026-004",
        "is_risk_spike": True
    },
    {
        "id": "EVT-009",
        "timestamp": "2026-02-14T21:30:00",
        "date_formatted": "14 Feb 2026",
        "time_formatted": "09:30 PM",
        "type": "SURVEILLANCE",
        "badge": "CRIME SCENE",
        "title": "Physical Handover Meeting at Andheri East",
        "description": "Delta-2 surveillance team observed Malhotra meeting Feroz Sheikh at Andheri warehouse. Metallic briefcase transferred.",
        "entities": ["P01", "P04", "L01", "V01"],
        "severity": "crit",
        "evidence_id": "EVID-2026-005",
        "is_risk_spike": True
    },
    {
        "id": "EVT-010",
        "timestamp": "2026-02-14T22:15:00",
        "date_formatted": "14 Feb 2026",
        "time_formatted": "10:15 PM",
        "type": "SURVEILLANCE",
        "badge": "VEHICLE SIGHTING",
        "title": "Vehicle Departure: MH-04 GK 7729",
        "description": "Vikram Solanki departed warehouse in vehicle MH-04 GK 7729 registered to Sanjay Verma. Corroborates 3-way syndicate tie.",
        "entities": ["P03", "V02", "P05", "L01"],
        "severity": "warn",
        "evidence_id": "EVID-2026-005",
        "is_risk_spike": True
    },
    {
        "id": "EVT-011",
        "timestamp": "2026-02-14T23:30:00",
        "date_formatted": "14 Feb 2026",
        "time_formatted": "11:30 PM",
        "type": "FIR",
        "badge": "FIR LODGED",
        "title": "FIR No. 031/2026 Formally Lodged",
        "description": "SI S. Deshmukh registered formal FIR 031/2026 at PS Andheri East naming Malhotra, Sheikh, and Shree Trading Co.",
        "entities": ["P01", "P04", "O01"],
        "severity": "warn",
        "evidence_id": "EVID-2026-001",
        "is_risk_spike": False
    }
]


@router.get("")
def get_timeline(
    case_id: str = "MH/CID/2026/0417",
    entity_id: Optional[str] = None,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Dedicated Investigation Timeline:
    Returns chronological timeline events with cross-source correlation,
    evidence citations, and timeline-linked risk spikes.
    """
    events = BASE_EVENTS.copy()

    # Filter by entity
    if entity_id:
        ent_clean = entity_id.upper()
        events = [e for e in events if any(ent_clean in ent.upper() for ent in e["entities"])]

    # Filter by event type
    if event_type:
        type_clean = event_type.upper()
        events = [e for e in events if e["type"] == type_clean]

    # Filter by date range
    if start_date:
        events = [e for e in events if e["timestamp"] >= start_date]
    if end_date:
        events = [e for e in events if e["timestamp"] <= end_date]

    # Annotate entity labels
    entity_names = {e.entity_id: e.label for e in db.query(Entity).all()}
    for ev in events:
        ev["entity_labels"] = [entity_names.get(e, e) for e in ev["entities"]]

    return {
        "case_id": case_id,
        "total_events": len(events),
        "filters_applied": {
            "entity_id": entity_id,
            "event_type": event_type,
            "start_date": start_date,
            "end_date": end_date
        },
        "timeline_events": sorted(events, key=lambda x: x["timestamp"])
    }


@router.get("/relationship-history")
def get_relationship_history(
    entity_a: str,
    entity_b: str,
    case_id: str = "MH/CID/2026/0417",
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Relationship History:
    Returns the temporal progression and sequence of interactions
    between any two specific entities over the course of the investigation.
    """
    pair = {entity_a.upper(), entity_b.upper()}

    history = [
        e for e in BASE_EVENTS
        if sum(1 for ent in e["entities"] if ent.upper() in pair) >= 2 or
           (entity_a.upper() in [ent.upper() for ent in e["entities"]] and
            entity_b.upper() in [ent.upper() for ent in e["entities"]])
    ]

    # Also search database edges for relationship details
    rel = db.query(Relationship).filter(
        Relationship.case_id == case_id,
        ((Relationship.source_id == entity_a) & (Relationship.target_id == entity_b)) |
        ((Relationship.source_id == entity_b) & (Relationship.target_id == entity_a))
    ).first()

    ent_a_rec = db.query(Entity).filter(Entity.entity_id == entity_a).first()
    ent_b_rec = db.query(Entity).filter(Entity.entity_id == entity_b).first()

    return {
        "case_id": case_id,
        "entity_a": {"id": entity_a, "label": ent_a_rec.label if ent_a_rec else entity_a},
        "entity_b": {"id": entity_b, "label": ent_b_rec.label if ent_b_rec else entity_b},
        "current_state": {
            "relationship_type": rel.rel_type if rel else "INDIRECT_ASSOCIATION",
            "weight": rel.weight if rel else None,
            "amount": rel.amount if rel else None,
            "backing_evidence_ids": json.loads(rel.evidence_ids or "[]") if rel else []
        },
        "interaction_events_count": len(history),
        "timeline_progression": history
    }
