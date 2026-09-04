"""
SUTRA Backend — routers/anomalies.py
====================================
Dedicated Anomaly & Risk Scoring Engine.
Delivers:
  - Deep risk decomposition (communication bursts, financial anomalies, centrality, reliability)
  - Timeline-linked risk indicators & spike intervals
  - Human verification enforcement
"""

import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db, RiskRecord, Entity, Relationship, EvidenceItem
from auth import require_role, TokenData

router = APIRouter()


@router.get("")
def list_anomalies(
    case_id: str = "MH/CID/2026/0417",
    min_score: float = Query(0, ge=0, le=100),
    entity_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """
    Dedicated Anomaly & Risk Page endpoint:
    Returns full mathematical decomposition of risk indicators for each entity,
    along with timeline-linked anomaly events.
    """
    records = db.query(RiskRecord).filter(
        RiskRecord.case_id == case_id,
        RiskRecord.risk_score >= min_score
    ).order_by(RiskRecord.risk_score.desc()).all()

    # Known timeline-linked spike timestamps per entity for investigative correlation
    timeline_spikes_map = {
        "P01": [
            {"timestamp": "2026-02-14T21:30:00", "type": "COMMUNICATION_BURST", "description": "18 calls in 48h to Feroz Sheikh prior to warehouse meeting", "evidence_id": "EVID-2026-004", "severity": "HIGH"},
            {"timestamp": "2026-02-12T15:20:00", "type": "FINANCIAL_OUTFLOW", "description": "₹18,40,000 NEFT transfer structured to Anita Rao", "evidence_id": "EVID-2026-003", "severity": "CRITICAL"},
            {"timestamp": "2026-02-14T22:45:00", "type": "SURVEILLANCE_MEETING", "description": "Physical meeting at Andheri East warehouse", "evidence_id": "EVID-2026-001", "severity": "HIGH"}
        ],
        "P02": [
            {"timestamp": "2026-02-12T15:20:00", "type": "FINANCIAL_INFLOW", "description": "High-velocity receipt of ₹18,40,000 without commercial invoice", "evidence_id": "EVID-2026-003", "severity": "CRITICAL"},
            {"timestamp": "2026-02-14T19:00:00", "type": "RAPID_COMMUNICATION", "description": "28 calls with Rajeev Malhotra immediately around fund movement", "evidence_id": "EVID-2026-004", "severity": "HIGH"}
        ],
        "P03": [
            {"timestamp": "2026-02-14T22:15:00", "type": "LOCATION_SURVEILLANCE", "description": "Arrival in vehicle MH-04 GK 7729 at warehouse handover", "evidence_id": "EVID-2026-005", "severity": "HIGH"},
            {"timestamp": "2026-01-18T11:05:00", "type": "CLEARING_TRANSFER", "description": "₹2,50,000 IMPS transfer to Rajeev Malhotra", "evidence_id": "EVID-2026-003", "severity": "MEDIUM"}
        ],
        "P04": [
            {"timestamp": "2026-02-14T21:30:00", "type": "BURST_COMMUNICATION", "description": "34 calls with Rajeev Malhotra, 14 late-night calls", "evidence_id": "EVID-2026-004", "severity": "HIGH"},
            {"timestamp": "2026-02-14T21:35:00", "type": "PHYSICAL_HANDOVER", "description": "Briefcase handover observed at Andheri warehouse", "evidence_id": "EVID-2026-005", "severity": "CRITICAL"}
        ],
        "P05": [
            {"timestamp": "2026-01-26T14:00:00", "type": "UNVERIFIED_CASH_LEASE", "description": "Informant report of cash lease for Bhiwandi godown", "evidence_id": "EVID-2026-002", "severity": "MEDIUM"}
        ]
    }

    results = []
    for r in records:
        b_down = json.loads(r.breakdown_json or "{}")
        ent = db.query(Entity).filter(Entity.entity_id == r.entity_id).first()

        spikes = timeline_spikes_map.get(r.entity_id, [])

        # Priority category
        if r.risk_score >= 50:
            tier = "CRITICAL_ATTENTION"
        elif r.risk_score >= 30:
            tier = "ELEVATED_RISK"
        else:
            tier = "LOW_MONITORED"

        results.append({
            "entity_id": r.entity_id,
            "name": r.name,
            "role": ent.role if ent else "Associate",
            "type": ent.type if ent else "person",
            "risk_indicator_score": r.risk_score,
            "tier": tier,
            "decomposition": {
                "communication_burst_anomaly": round(b_down.get("communication_anomaly", 0) * 100, 1),
                "financial_velocity_anomaly": round(b_down.get("financial_anomaly", 0) * 100, 1),
                "network_centrality_weight": round(b_down.get("network_centrality", 0) * 100, 1),
                "temporal_clustering": round(b_down.get("temporal_proximity", 1.0) * 100, 1),
                "geographic_correlation": round(b_down.get("location_correlation", 1.0) * 100, 1),
                "source_reliability_factor": b_down.get("source_reliability_multiplier", 1.0)
            },
            "timeline_spikes_count": len(spikes),
            "timeline_spikes": spikes,
            "requires_human_verification": True
        })

    return {
        "case_id": case_id,
        "total_evaluated": len(results),
        "disclaimer": "All risk scores are calculated decision-support indicators and DO NOT constitute proof of guilt. All leads require human verification.",
        "risk_indicators": results
    }


@router.get("/decomposition/{entity_id}")
def get_entity_risk_decomposition(
    entity_id: str,
    case_id: str = "MH/CID/2026/0417",
    db: Session = Depends(get_db),
    user: TokenData = Depends(require_role("analyst"))
):
    """Deep-dive mathematical risk breakdown for a single suspect."""
    record = db.query(RiskRecord).filter(
        RiskRecord.case_id == case_id,
        RiskRecord.entity_id == entity_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Entity risk record not found")

    ent = db.query(Entity).filter(Entity.entity_id == entity_id).first()
    b_down = json.loads(record.breakdown_json or "{}")

    return {
        "case_id": case_id,
        "entity_id": entity_id,
        "name": record.name,
        "role": ent.role if ent else "Associate",
        "composite_score": record.risk_score,
        "formula": "Risk = 0.35 * CommAnomaly + 0.30 * FinAnomaly + 0.20 * Centrality + 0.15 * TemporalGeo",
        "breakdown": b_down,
        "requires_human_verification": True
    }
