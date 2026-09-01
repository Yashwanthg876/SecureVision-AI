import logging
from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.dashboard import (
    SummaryKPI,
    ThreatTrendDataPoint,
    RiskDistribution,
    RecentActivity,
    CriticalFinding
)
from app.services.auth import get_current_user
from app.core.responses import StandardResponse, success_response
from app.database.database import get_db
from app.services.dashboard.dashboard_service import dashboard_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/summary", response_model=StandardResponse[SummaryKPI])
def get_dashboard_summary(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get genuine aggregated high-level KPIs from database tables.
    """
    user_id = str(current_user.id) if current_user else "guest_user"
    data = dashboard_service.get_summary(db, user_id)
    return success_response(data, request.state.request_id)

@router.get("/threat-trend", response_model=StandardResponse[List[ThreatTrendDataPoint]])
def get_threat_trend(request: Request, days: int = 7, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get real threat trend data computed from user scans over the past N days.
    """
    user_id = str(current_user.id) if current_user else "guest_user"
    data = dashboard_service.get_threat_trend(db, user_id, days)
    return success_response(data, request.state.request_id)

@router.get("/risk-distribution", response_model=StandardResponse[List[RiskDistribution]])
def get_risk_distribution(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get genuine risk distribution computed from user scan database findings.
    """
    user_id = str(current_user.id) if current_user else "guest_user"
    data = dashboard_service.get_risk_distribution(db, user_id)
    return success_response(data, request.state.request_id)

@router.get("/recent-activity", response_model=StandardResponse[List[RecentActivity]])
def get_recent_activity(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get real recent system activities logged across Website, GitHub, and AI modules.
    """
    user_id = str(current_user.id) if current_user else "guest_user"
    data = dashboard_service.get_recent_activity(db, user_id)
    return success_response(data, request.state.request_id)

@router.get("/critical-findings", response_model=StandardResponse[List[CriticalFinding]])
def get_critical_findings(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get genuine critical findings from database tables that require attention.
    """
    user_id = str(current_user.id) if current_user else "guest_user"
    data = dashboard_service.get_critical_findings(db, user_id)
    return success_response(data, request.state.request_id)
