from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from backend.app.models.domain import UserRole, AuditStatus

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


# Audit & Compliance Payload Schemas

class AuditLogRequest(BaseModel):
    transaction_reference: str = Field(..., max_length=100, example="TXN-90218")
    raw_payload: str = Field(..., description="Raw execution context or prompt payload submitted to downstream agent frameworks.")

class AuditLogResponse(BaseModel):
    id: UUID
    transaction_reference: str
    compliance_status: AuditStatus
    latency_ms: int
    token_cost: float
    eval_score: Optional[float]
    meta_data: Dict[str, Any]
    created_at: datetime
    # user_id: Optional[UUID]
    # raw_payload: str
    # cleaned_payload: Optional[str]
    model_config = {"from_attributes": True}
