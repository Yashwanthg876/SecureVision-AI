import logging
from typing import Any, Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth import get_current_user
from app.schemas.threat_intel import IOCLookupRequest, IOCLookupResponse, ThreatIntelStatsResponse
from app.services.threat_intelligence.threat_intel_service import threat_intel_service
from app.core.responses import StandardResponse, success_response
from app.core.exceptions import SecureVisionException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/feed", response_model=StandardResponse)
async def get_threat_feed(
    req: Request,
    limit: int = Query(default=50, ge=1, le=100),
    severity: Optional[str] = Query(default=None),
    ioc_type: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get filterable global threat intelligence feed items.
    """
    try:
        items = threat_intel_service.get_feed(
            db=db,
            limit=limit,
            severity=severity,
            ioc_type=ioc_type,
            search_query=q,
        )
        return success_response({"items": [item.model_dump() for item in items]}, req.state.request_id)
    except Exception as e:
        logger.error(f"Failed to fetch threat intelligence feed: {e}", exc_info=True)
        raise SecureVisionException("Failed to retrieve threat intelligence feed.", status_code=500)

@router.post("/lookup", response_model=StandardResponse[IOCLookupResponse])
async def lookup_ioc(
    req: Request,
    body: IOCLookupRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Perform an instant lookup and reputation analysis on an IP, Domain, Hash, URL, or CVE ID.
    """
    if not body.query or not body.query.strip():
        raise SecureVisionException("Lookup query cannot be empty.", status_code=400)

    try:
        res = await threat_intel_service.lookup_ioc(db, body.query)
        return success_response(res, req.state.request_id)
    except Exception as e:
        logger.error(f"Threat IOC lookup failed: {e}", exc_info=True)
        raise SecureVisionException("IOC lookup failed due to an internal error.", status_code=500)

@router.get("/stats", response_model=StandardResponse[ThreatIntelStatsResponse])
async def get_threat_stats(
    req: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get aggregated threat metrics, category distribution, and top threat vectors.
    """
    try:
        stats = threat_intel_service.get_stats(db)
        return success_response(stats, req.state.request_id)
    except Exception as e:
        logger.error(f"Failed to compute threat statistics: {e}", exc_info=True)
        raise SecureVisionException("Failed to fetch threat intelligence statistics.", status_code=500)
