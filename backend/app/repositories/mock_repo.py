# System User Mock Storage Blueprint
from typing import Optional
from backend.app.models.domain import DBUser, UserRole
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MockUserRepository:
    """Simulates production credential lookup structures for deployment validation runs."""
    @staticmethod
    async def get_mock_user_by_email(email: str) -> Optional[DBUser]:
        if email == "compliance.officer@ubs-mock.com":
            return DBUser(
                id=uuid.UUID("a6b0c231-1bf3-4b68-b76b-95689104f1a2"),
                email="compliance.officer@ubs-mock.com",
                hashed_password=pwd_context.hash("GuardShield2026!"),
                full_name="Sarah Jenkins",
                role=UserRole.COMPLIANCE_OFFICER,
                is_active=True
            )
        elif email == "risk.analyst@ubs-mock.com":
            return DBUser(
                id=uuid.UUID("b4d1c932-2cf4-5c79-c87c-06790215f2b3"),
                email="risk.analyst@ubs-mock.com",
                hashed_password=pwd_context.hash("GuardShield2026!"),
                full_name="David Miller",
                role=UserRole.RISK_ANALYST,
                is_active=True
            )
        return None