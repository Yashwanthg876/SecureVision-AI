from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from app.schemas.website_security import AssessmentRequest, AssessmentResponse
from app.services.website_security import assessment_service
from app.services.auth import get_current_user
from app.database.database import get_db
from app.core.responses import StandardResponse, success_response
from app.core.exceptions import AssessmentNotFoundError, SecureVisionException
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scan", response_model=StandardResponse[AssessmentResponse])
async def run_website_assessment(
    request: AssessmentRequest, 
    req: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes a comprehensive, passive website security assessment live on the target URL.
    Persists results to DB.
    """
    user_id = str(current_user.id)
    try:
        result = await assessment_service.perform_assessment(request.url, db, user_id)
        return success_response(result, req.state.request_id)
    except ValueError as ve:
        raise SecureVisionException(str(ve), status_code=400)

@router.get("/history", response_model=StandardResponse)
async def get_assessment_history(
    req: Request,
    domain: str = Query(None),
    risk_level: str = Query(None),
    status: str = Query(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns a list of previous assessments.
    """
    user_id = current_user.id
    data = assessment_service.get_assessment_history(db, user_id, domain, risk_level, status)
    return success_response({"items": data}, req.state.request_id)

@router.get("/timeline", response_model=StandardResponse)
async def get_assessment_timeline(
    req: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns chronological score data for trend charts.
    """
    user_id = current_user.id
    data = assessment_service.get_assessment_timeline(db, user_id)
    return success_response(data, req.state.request_id)

@router.get("/compare", response_model=StandardResponse)
async def compare_assessments(
    req: Request,
    id1: str = Query(None),
    id2: str = Query(None),
    domain: str = Query(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compares two assessments. Pass either id1 and id2, OR pass domain to compare the two most recent runs.
    """
    user_id = current_user.id
    data = assessment_service.compare_assessments(db, user_id, id1, id2, domain)
    return success_response(data, req.state.request_id)

@router.get("/history/{id}", response_model=StandardResponse)
async def get_assessment_by_id(
    id: str,
    req: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns full details for a single assessment.
    """
    user_id = current_user.id
    data = assessment_service.get_assessment_by_id(db, user_id, id)
    return success_response(data, req.state.request_id)
