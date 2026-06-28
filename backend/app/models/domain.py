from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from backend.app.repositories.base import Base
from sqlalchemy import Column, String, DateTime, Numeric, Boolean, Integer, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
import enum

class UserRole(str, enum.Enum):
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"
    RISK_ANALYST = "RISK_ANALYST"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"

class AuditStatus(str, enum.Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED_GUARDRAIL = "FAILED_GUARDRAIL"
    MANUAL_REVIEW = "MANUAL_REVIEW"

class DBUser(Base):
    __tablename__ = "system_users"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, index=True, default=UUID)
    full_name: str = Column(String, unique=True, nullable=False)
    email: str = Column(String(255), unique=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    role: str = Column(SqlEnum(UserRole), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

def DBAuditLog(Base):
    __tablename__ = "audit_logs"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=UUID)
    user_id: UUID = Column(PGUUID(as_uuid=True), nullable=True)
    transaction_reference: str = Column(String(100), unique=True, nullable=False)
    raw_payload: str = Column(String, nullable=False)
    cleaned_payload: str = Column(String, nullable=True)
    compliance_status: str = Column(SqlEnum(AuditStatus), default=AuditStatus.MANUAL_REVIEW, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    token_cost = Column(Numeric(10, 5), default=0.0)
    eval_score = Column(Numeric(5, 2), nullable=True)
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

