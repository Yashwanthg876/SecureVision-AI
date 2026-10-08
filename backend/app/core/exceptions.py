from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.responses import error_response
import logging

logger = logging.getLogger(__name__)

class SecureVisionException(Exception):
    """Base exception for all domain-specific exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AssessmentNotFoundError(SecureVisionException):
    def __init__(self, assessment_id: str):
        super().__init__(f"Assessment with ID {assessment_id} not found.", status_code=404)

class AIModelError(SecureVisionException):
    def __init__(self, model_name: str, detail: str):
        super().__init__(f"AI Model {model_name} failed: {detail}", status_code=500)

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches all unhandled exceptions and formats them into the standard ResponseSchema.
    """
    request_id = getattr(request.state, "request_id", None)
    
    if isinstance(exc, SecureVisionException):
        logger.warning(f"Domain Exception [{request_id}]: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.message, request_id).model_dump()
        )

    if isinstance(exc, StarletteHTTPException):
        logger.warning(f"HTTP Exception [{request_id}] {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.detail, request_id).model_dump()
        )

    if isinstance(exc, RequestValidationError):
        logger.warning(f"Validation Error [{request_id}]: {exc.errors()}")
        first_error = exc.errors()[0] if exc.errors() else {"msg": "Invalid request payload"}
        err_msg = f"{first_error.get('loc', ['field'])[-1]}: {first_error.get('msg', 'Validation error')}"
        return JSONResponse(
            status_code=422,
            content=error_response(err_msg, request_id).model_dump()
        )
        
    logger.error(f"Unhandled Exception [{request_id}]: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response("Internal Server Error", request_id).model_dump()
    )
