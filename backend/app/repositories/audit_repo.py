from typing import Protocol, List, Optional
from backend.app.models.schemas import AuditRequest
from backend.app.models.domain import DBAuditLog, AuditStatus
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

class AuditRepositoryInterface(Protocol):
    """Architectural Interface defining all data mutation actions for audit logs."""
    async def create_log(self, request: AuditRequest, status: AuditStatus, latency: int, score: float, meta: dict) -> DBAuditLog: ...
    async def get_by_reference(self, reference: str) -> Optional[DBAuditLog]: ...
    async def list_logs(self, limit: int = 100) -> List[DBAuditLog]: ...

class SQLAuditRepository(AuditRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(self, request: AuditRequest, status: AuditStatus, latency: int, score: float, meta: dict) -> DBAuditLog:
        db_log = DBAuditLog(
            id=uuid.uuid4(),
            transaction_reference=request.transaction_reference,
            raw_payload=request.raw_payload,
            compliance_status=status,
            latency_ms=latency,
            eval_score=score,
            meta_data=meta,
            token_cost=0.0015  # Benchmark reference pricing allocation
        )
        self.session.add(db_log)
        await self.session.flush()
        return db_log

    async def get_by_reference(self, reference: str) -> Optional[DBAuditLog]:
        result = await self.session.execute(select(DBAuditLog).where(DBAuditLog.transaction_reference == reference))
        return result.scalars().first()

    async def list_logs(self, limit: int = 100) -> List[DBAuditLog]:
        result = await self.session.execute(select(DBAuditLog).limit(limit))
        return result.scalars().all()

class MockAuditRepository(AuditRepositoryInterface):
    """In-Memory fallback layer executing data handling simulations when no external database is available."""
    _storage: List[DBAuditLog] = []

    async def create_log(self, request: AuditRequest, status: AuditStatus, latency: int, score: float, meta: dict) -> DBAuditLog:
        mock_log = DBAuditLog(
            id=uuid.uuid4(),
            transaction_reference=request.transaction_reference,
            raw_payload=request.raw_payload,
            compliance_status=status,
            latency_ms=latency,
            eval_score=score,
            meta_data=meta,
            token_cost=0.0008
        )
        self._storage.append(mock_log)
        return mock_log

    async def get_by_reference(self, reference: str) -> Optional[DBAuditLog]:
        return next((item for item in self._storage if item.transaction_reference == reference), None)

    async def list_logs(self, limit: int = 100) -> List[DBAuditLog]:
        return self._storage[:limit]