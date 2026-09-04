"""
SUTRA Backend — database.py
===========================
SQLite + SQLAlchemy database layer for persistent case data, Evidence Vault,
entities, graph relationships, audit logs, ingestion jobs, and risk scores.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DB_PATH = Path(__file__).resolve().parent / "sutra.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"

    case_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    status = Column(String, default="active")
    created_by = Column(String, default="demo_investigator")
    created_at = Column(DateTime, default=datetime.utcnow)

    evidence_items = relationship("EvidenceItem", back_populates="case", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="case", cascade="all, delete-orphan")
    relationships = relationship("Relationship", back_populates="case", cascade="all, delete-orphan")
    ingestions = relationship("IngestionJob", back_populates="case", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="case", cascade="all, delete-orphan")


class EvidenceItem(Base):
    __tablename__ = "evidence_vault"

    evidence_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # FIR, CDR, BANK_RECORD, SURVEILLANCE, FIELD_REPORT
    source_agency = Column(String, default="Maharashtra Police CID")
    officer_name = Column(String, default="Insp. V. Kadam")
    sha256_hash = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    content_text = Column(Text, default="")
    provenance_chain = Column(Text, default="[]")  # JSON list of custody transfers
    reliability_score = Column(Float, default=0.9)  # 0.0 to 1.0 (High=0.9, Medium=0.7, Low=0.4)
    verified_status = Column(String, default="verified")  # verified, pending, flagged
    verified_by = Column(String, default="System Initializer")
    verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="evidence_items")

    @classmethod
    def compute_hash(cls, content: str | bytes) -> str:
        if isinstance(content, str):
            content = content.encode("utf-8")
        return hashlib.sha256(content).hexdigest()


class Entity(Base):
    __tablename__ = "entities"

    entity_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    label = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # person, phone, organization, vehicle, location, account, document
    role = Column(String, default="Associate")
    aliases = Column(Text, default="[]")  # JSON list
    attributes_json = Column(Text, default="{}")  # JSON object
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="entities")


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    source_id = Column(String, index=True, nullable=False)
    target_id = Column(String, index=True, nullable=False)
    rel_type = Column(String, nullable=False)  # CALLED, TRANSFERRED_MONEY, VISITED, OWNS, WORKS_FOR, ASSOCIATED_WITH
    weight = Column(Integer, default=1)
    amount = Column(Float, nullable=True)
    notes = Column(Text, default="")
    evidence_ids = Column(Text, default="[]")  # JSON list of linked Evidence IDs (e.g. ["EVID-2026-001"])
    timestamp = Column(String, nullable=True)  # ISO timestamp of interaction

    case = relationship("Case", back_populates="relationships")


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    job_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, default=0)
    sha256_hash = Column(String, nullable=True)
    status = Column(String, default="completed")  # queued, processing, completed, failed
    current_stage = Column(String, default="6_GRAPH_RISK_INDEXING")
    stage_logs = Column(Text, default="[]")  # JSON array of stage results
    extracted_counts = Column(Text, default="{}")  # JSON {entities: 5, relationships: 4}
    evidence_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="ingestions")


class ResolutionCandidate(Base):
    __tablename__ = "resolution_candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    source_mention = Column(String, nullable=False)
    target_mention = Column(String, nullable=False)
    suggested_entity_id = Column(String, nullable=True)
    similarity_score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    shared_attributes = Column(Text, default="[]")  # JSON array (e.g. ["shared phone", "shared vehicle"])
    status = Column(String, default="pending")  # pending, approved, rejected
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)


class RiskRecord(Base):
    __tablename__ = "risk_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    entity_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    risk_score = Column(Integer, default=0)
    breakdown_json = Column(Text, default="{}")
    factors_json = Column(Text, default="{}")
    calculated_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    username = Column(String, nullable=False)
    role = Column(String, default="investigator")
    action_type = Column(String, nullable=False)  # EVIDENCE_VERIFIED, ENTITY_MERGED, SHORTEST_PATH_QUERY, AI_QUERY, etc.
    target_id = Column(String, nullable=True)
    details_json = Column(Text, default="{}")

    case = relationship("Case", back_populates="audit_logs")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
