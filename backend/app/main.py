from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.exceptions import register_exception_handlers
from backend.app.api.middleware.guardrails import GuardrailMiddleware
from backend.app.api.middleware.telemetry import OpenTelemetryMetricsMiddleware
from backend.app.api.v1 import auth, compliance

def create_app() -> FastAPI:
    """Configures and returns the initialized enterprise application gateway instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Enterprise multi-agent risk evaluation and regulatory compliance auditing architecture.",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # 1. Security Configuration: Enforce strict CORS policies
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict to verified enterprise internal sub-domains in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 2. Operations Architecture Middleware
    app.add_middleware(GuardrailMiddleware)
    app.add_middleware(OpenTelemetryMetricsMiddleware)
    
    # 3. Exception Boundaries Registration
    register_exception_handlers(app)
    
    # 4. Route Routing Map Directives
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Identity & Access Management"])
    app.include_router(compliance.router, prefix=f"{settings.API_V1_STR}/compliance", tags=["Compliance Operations Ledger"])
    
    @app.get("/health", tags=["Infrastructure Utility System Checks"])
    async def health_check():
        """Exposes operational status indicators to Kubernetes liveness probes."""
        return {
            "status": "healthy",
            "persistence_mode": "PostgreSQL Async Driver" if settings.USE_DATABASE else "In-Memory Mock Repository",
            "environment": settings.ENVIRONMENT
        }
        
    return app

app = create_app()