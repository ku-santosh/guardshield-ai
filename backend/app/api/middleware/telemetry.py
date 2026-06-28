import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.trace import Tracer
from backend.app.core.logging import system_logger

# Initialize global tracer context reference
tracer: Tracer = trace.get_tracer("guardshield.telemetry.middleware")

class OpenTelemetryMetricsMiddleware(BaseHTTPMiddleware):
    """
    Provides precise runtime latency instrumentation, tracking request lifecycles 
    and exposing performance metrics for monitoring tools like Prometheus and Grafana.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        path_name = request.url.path
        method_type = request.method
        
        # Open an independent execution span context window
        with tracer.start_as_current_span(f"HTTP {method_type} {path_name}") as span:
            span.set_attribute("http.method", method_type)
            span.set_attribute("http.route", path_name)
            
            try:
                response = await call_next(request)
                duration = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
                
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.duration_ms", duration)
                
                # Log structured performance data for analysis
                system_logger.info(
                    f"Request completed: {method_type} {path_name} -> Status: {response.status_code}",
                    extra_context={
                        "http_method": method_type,
                        "http_path": path_name,
                        "status_code": response.get("status_code", response.status_code),
                        "latency_ms": round(duration, 2)
                    }
                )
                return response
                
            except Exception as ex:
                duration = (time.perf_counter() - start_time) * 1000
                span.record_exception(ex)
                span.set_status(trace.StatusCode.ERROR, str(ex))
                
                system_logger.error(
                    f"Request failed pipeline processing: {method_type} {path_name} -> {str(ex)}",
                    extra_context={
                        "http_method": method_type,
                        "http_path": path_name,
                        "latency_ms": round(duration, 2),
                        "error_message": str(ex)
                    }
                )
                raise ex