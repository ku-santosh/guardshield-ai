from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from backend.app.core.logging import system_logger

class GuardShieldBaseException(Exception):
    """Root error class for all domain-specific application anomalies."""
    def __init__(self, message: str, diagnostic_code: str = "GENERIC_ERROR"):
        self.message = message
        self.diagnostic_code = diagnostic_code
        super().__init__(self.message)

class ComplianceEvaluationException(GuardShieldBaseException):
    """Raised when an automated quality evaluation gate fails processing requirements."""
    pass

class UnauthorizedAgentInvocationException(GuardShieldBaseException):
    """Raised when an execution context attempts to invoke a tool without the required RBAC clearance level."""
    pass

def register_exception_handlers(app: FastAPI) -> None:
    """Binds global error handling wrappers to the application router framework."""
    
    @app.exception_handler(GuardShieldBaseException)
    async def domain_exception_handler(request: Request, exc: GuardShieldBaseException):
        system_logger.error(f"Application domain anomaly caught: [{exc.diagnostic_code}] {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": exc.diagnostic_code,
                "message": exc.message,
                "context_path": request.url.path
            }
        )

    @app.exception_handler(Exception)
    async def global_unhandled_exception_handler(request: Request, exc: Exception):
        system_logger.critical(f"System panic caught in event loop: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "INTERNAL_SYSTEM_PANIC",
                "message": "A critical system anomaly occurred. Engineers have been notified via telemetry tracking lines."
            }
        )