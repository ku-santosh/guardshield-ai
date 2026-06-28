import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.schemas import AuditRequest, AuditLogResponse
from backend.app.core.security import RoleChecker
from backend.app.models.domain import UserRole, AuditStatus
from backend.app.repositories.base import get_db_session
from backend.app.repositories.audit_repo import SQLAuditRepository, MockAuditRepository
from backend.app.agents.orchestrator import GuardShieldMultiAgentOrchestrator
from backend.app.core.config import settings

router = APIRouter()
orchestrator = GuardShieldMultiAgentOrchestrator()

@router.post("/audit", response_model=AuditLogResponse, dependencies=[Depends(RoleChecker([UserRole.RISK_ANALYST, UserRole.COMPLIANCE_OFFICER]))])
async def execute_transaction_audit(request: AuditRequest, db: AsyncSession = Depends(get_db_session)):
    """
    Executes a multi-agent compliance review on incoming payloads.
    Uses database factories via repository patterns to support standalone runs without SQL dependencies.
    """
    start_time = time.perf_counter()
    
    # 1. Instantiate the correct repository pattern variant based on configuration settings
    if settings.USE_DATABASE and db:
        repo = SQLAuditRepository(db)
    else:
        repo = MockAuditRepository()

    # Check for existing logs to prevent duplicate operations
    existing_record = await repo.get_by_reference(request.transaction_reference)
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate Transaction Exception: This reference identifier is already locked inside system logs."
        )

    try:
        # 2. Run the Multi-Agent Evaluation Orchestrator
        scorecard = await orchestrator.process_compliance_audit(request.transaction_reference, request.raw_payload)
        
        # Map qualitative assessments to formal database enums
        mapped_status = AuditStatus.PASSED if scorecard.is_compliant else AuditStatus.WARNING
        if scorecard.risk_score > 0.75:
            mapped_status = AuditStatus.MANUAL_REVIEW

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        # 3. Persist the audit log
        meta_payload = {
            "justification": scorecard.justification,
            "engine_orchestrator": "AutoGen + Pydantic AI Core Bundle",
            "version_tag": "2026.1"
        }
        
        saved_record = await repo.create_log(
            request=request,
            status=mapped_status,
            latency=latency_ms,
            score=scorecard.risk_score,
            meta=meta_payload
        )
        
        return saved_record

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during multi-agent analysis: {str(ex)}"
        )