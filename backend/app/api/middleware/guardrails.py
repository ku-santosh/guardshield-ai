import re
import time
from typing import Dict, Any, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from backend.app.core.logging import system_logger

class GuardrailSecurityEngine:
    """
    High-performance validation processor for detecting adversarial execution patterns 
    and enforcing strict content privacy rules on incoming data streams.
    """
    
    # Pre-compiled high-speed evaluation regular expressions
    INJECTION_PATTERNS = [
        re.compile(r"ignore\s+previous\s+instructions", re.IGNORECASE),
        re.compile(r"system\s+prompt\s+override", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+an\s+unrestricted", re.IGNORECASE),
        re.compile(r"bypass\s+all\s+guardrails", re.IGNORECASE),
        re.compile(r"<\s*script\s*>", re.IGNORECASE)
    ]
    
    # Target entities for automated PII masking
    CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    @classmethod
    def scan_for_prompt_injection(cls, payload: str) -> bool:
        """Evaluates payloads against active adversarial attack vectors."""
        return any(pattern.search(payload) for pattern in cls.INJECTION_PATTERNS)

    @classmethod
    def scrub_pii_data(cls, payload: str) -> Tuple[str, int]:
        """
        Locates and replaces private user attributes with generic tokens.
        Returns a tuple containing the scrubbed text and total modifications made.
        """
        modifications = 0
        scrubbed = payload
        
        # Mask payment cards
        cards_found = cls.CREDIT_CARD_PATTERN.findall(scrubbed)
        if cards_found:
            modifications += len(cards_found)
            scrubbed = cls.CREDIT_CARD_PATTERN.sub("[REDACTED_CONFIDENTIAL_CARD]", scrubbed)
            
        # Mask routing emails
        emails_found = cls.EMAIL_PATTERN.findall(scrubbed)
        if emails_found:
            modifications += len(emails_found)
            scrubbed = cls.EMAIL_PATTERN.sub("[REDACTED_IDENTITY_EMAIL]", scrubbed)
            
        return scrubbed, modifications

class GuardrailMiddleware(BaseHTTPMiddleware):
    """Intercepts incoming API calls to enforce real-time protection guardrails."""
    async def dispatch(self, request: Request, call_next) -> Response:
        # Only process telemetry rules on compliance audit endpoints
        if "/api/v1/compliance/audit" in request.url.path and request.method == "POST":
            try:
                # Read body content safely without draining the request stream
                body_bytes = await request.body()
                body_str = body_bytes.decode("utf-8")
                
                # 1. Evaluate prompt injection risk
                if GuardrailSecurityEngine.scan_for_prompt_injection(body_str):
                    system_logger.error("Security alert: Prompt injection attack intercepted", extra_context={"path": request.url.path})
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Security Violation: Malicious payload modification patterns detected."}
                    )
                
                # 2. Run background PII data sanitization
                scrubbed_str, mod_count = GuardrailSecurityEngine.scrub_pii_data(body_str)
                if mod_count > 0:
                    # Re-bind the sanitized string back into the request context receiver
                    async def receive_wrapper():
                        return {"type": "http.request", "body": scrubbed_str.encode("utf-8"), "more_body": False}
                    request._receive = receive_wrapper
                    system_logger.info(f"Compliance Engine scrubbed {mod_count} PII identifiers from payload.")
                    
            except Exception as ex:
                system_logger.error(f"Guardrail middleware pipeline failure: {str(ex)}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "Internal verification processing error."}
                )
                
        return await call_next(request)