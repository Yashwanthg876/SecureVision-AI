import logging
from typing import Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth import get_current_user
from app.schemas.ai_detection import AIDetectionRequest, AIDetectionResponse
from app.services.ai_detection.analyzer import ai_analyzer
from app.repositories.ai_detection_repository import ai_detection_repository
from app.core.responses import StandardResponse, success_response
from app.core.exceptions import SecureVisionException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scan", response_model=StandardResponse[AIDetectionResponse])
async def scan_ai_content(
    req: Request,
    body: AIDetectionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Scan text or code to detect AI-generated patterns, calculate perplexity and burstiness.
    """
    user_id = str(current_user.id)
    if not body.content or not body.content.strip():
        raise SecureVisionException("Content cannot be empty.", status_code=400)
        
    try:
        result = ai_analyzer.analyze(body.content, body.content_type, db, user_id)
        return success_response(result, req.state.request_id)
    except Exception as e:
        logger.error(f"AI detection scan failed: {e}", exc_info=True)
        raise SecureVisionException("Scan failed due to an unexpected error. Please try again.", status_code=500)

@router.get("/history", response_model=StandardResponse)
async def get_ai_detection_history(
    req: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Return the AI detection scan history for the current user.
    """
    user_id = str(current_user.id)
    scans = ai_detection_repository.get_by_user(db, user_id)
    data = [
        {
            "id": str(s.id),
            "content_snippet": s.content_snippet,
            "content_type": s.content_type,
            "ai_probability": s.ai_probability,
            "risk_level": s.risk_level,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else "",
        }
        for s in scans
    ]
    return success_response({"items": data}, req.state.request_id)
