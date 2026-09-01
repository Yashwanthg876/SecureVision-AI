from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from datetime import datetime

T = TypeVar('T')

class ResponseMeta(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    request_id: Optional[str] = None
    version: str = "1.0.0"

class StandardResponse(BaseModel, Generic[T]):
    """
    Unified API response wrapper. Every API endpoint should return this schema.
    """
    success: bool
    data: Optional[T] = None
    error: Optional[Any] = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
    
def success_response(data: Any, request_id: str = None) -> StandardResponse:
    meta = ResponseMeta(request_id=request_id) if request_id else ResponseMeta()
    return StandardResponse(success=True, data=data, meta=meta)
    
def error_response(error_detail: Any, request_id: str = None) -> StandardResponse:
    meta = ResponseMeta(request_id=request_id) if request_id else ResponseMeta()
    return StandardResponse(success=False, error=error_detail, meta=meta)
