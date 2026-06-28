import pytest
from httpx import AsyncClient
from backend.app.main import app
from backend.app.core.config import settings

@pytest.mark.asyncio
async def test_health_endpoint():
    """Verifies that the primary system status interface is healthy and reporting correctly."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_unauthenticated_audit_rejection():
    """Verifies that client access is blocked with an HTTP 401 Unauthorized error when no bearer token is present."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/compliance/audit",
            json={"transaction_reference": "TXN-ERR", "raw_payload": "Data payload context"}
        )
    assert response.status_code == 401