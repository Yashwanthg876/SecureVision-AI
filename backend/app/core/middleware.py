import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import setup_logger

logger = setup_logger("middleware")

class EnterpriseMiddleware(BaseHTTPMiddleware):
    """
    Injects request IDs, logs execution time, and records access logs.
    """
    async def dispatch(self, request: Request, call_next):
        supplied_request_id = request.headers.get("X-Request-ID", "")
        request_id = supplied_request_id if supplied_request_id.isascii() and supplied_request_id.isalnum() and len(supplied_request_id) <= 64 else str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        # We can inject request_id into a context variable if we want it globally available
        # For now, we pass it down the request scope.
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
            
            logger.info(
                f"Completed {request.method} {request.url.path}",
                extra={"request_id": request_id, "process_time_ms": round(process_time * 1000, 2), "status_code": response.status_code}
            )
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Failed {request.method} {request.url.path}",
                extra={"request_id": request_id, "process_time_ms": round(process_time * 1000, 2), "error": str(e)}
            )
            raise # Let global_exception_handler catch it
