from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    investigator = "investigator"
    senior_investigator = "senior_investigator"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer, nullable=False)
    account_status = Column(String, default="active")
    organization = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, index=True) # E.g., C-0417
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="open") # open, closed, archived
    jurisdiction = Column(String, nullable=True)
    sensitivity = Column(String, default="standard") # standard, confidential, restricted
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    created_by = relationship("User")
    evidence = relationship("Evidence", back_populates="case")
    audit_logs = relationship("AuditLog", back_populates="case")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, index=True) # E.g., E-1042
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    source = Column(String, nullable=True)
    hash_algorithm = Column(String, default="SHA-256")
    sha256_hash = Column(String, nullable=False)
    integrity_status = Column(String, default="unverified") # unverified, verified, mismatch
    provenance_status = Column(String, default="registered")
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Store linked graph object IDs as JSON arrays (since actual objects are in Neo4j)
    linked_entities = Column(JSON, default=list)
    linked_relationships = Column(JSON, default=list)
    linked_events = Column(JSON, default=list)
    linked_risk_signals = Column(JSON, default=list)

    case = relationship("Case", back_populates="evidence")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String, nullable=True)
    action = Column(String, nullable=False) # VIEWED, MERGED, VERIFIED, UPLOADED
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    case_id = Column(String, ForeignKey("cases.id"), nullable=True)
    object_type = Column(String, nullable=False) # Evidence, Case, Entity, Risk Signal
    object_id = Column(String, nullable=False)
    previous_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    reason = Column(Text, nullable=True)
    session_id = Column(String, nullable=True)

    actor = relationship("User")
    case = relationship("Case", back_populates="audit_logs")
