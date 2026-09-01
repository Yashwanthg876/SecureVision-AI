import logging
from typing import Any, Optional
from fastapi import APIRouter, Depends, Response, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.services.auth import get_current_user
from app.database.database import get_db
from app.services.reports.report_service import generate_report, list_user_reports
from app.repositories.assessment_repository import assessment_repository
from app.core.exceptions import SecureVisionException, AssessmentNotFoundError
from app.core.responses import StandardResponse, success_response

router = APIRouter()
logger = logging.getLogger(__name__)

class ReportGenerateRequest(BaseModel):
    assessment_id: Optional[str] = None
    target_domain: Optional[str] = Field(default="api.securevision.ai")
    report_type: str = Field(default="Executive Summary", pattern="^(Executive Summary|Technical Audit|OWASP Top 10)$")
    format_type: str = Field(default="pdf", pattern="^(?i:pdf|csv|json)$")

@router.get("", response_model=StandardResponse)
async def get_reports_list(
    req: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get list of available assessment reports for current user or guest.
    """
    user_id = current_user.id
    reports = list_user_reports(db, user_id)
    return success_response({"items": reports}, req.state.request_id)

@router.post("/generate", response_model=StandardResponse)
async def create_on_demand_report(
    req: Request,
    body: ReportGenerateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Generate or export a security report on demand.
    """
    user_id = current_user.id
    
    # If specific assessment ID passed, check it
    target_id = body.assessment_id
    if not target_id:
        assessments = assessment_repository.get_user_assessments(db, user_id=user_id)
        if assessments:
            target_id = str(assessments[0].id)
            
    if not target_id:
        raise SecureVisionException("No valid security assessment found to generate report.", status_code=400)
    assessment = assessment_repository.get(db, target_id)
    if not assessment or assessment.is_deleted or assessment.user_id != user_id:
        raise AssessmentNotFoundError(target_id)
        
    return success_response({
        "assessment_id": target_id,
        "format": body.format_type,
        "report_type": body.report_type,
        "download_url": f"/api/v1/reports/{target_id}/{body.format_type.lower()}",
        "status": "Ready"
    }, req.state.request_id)

@router.get("/{assessment_id}/pdf")
async def get_pdf_report(
    assessment_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    try:
        buffer = generate_report(assessment_id, 'pdf', db, user_id)
        return StreamingResponse(
            buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename=SecureVision_Report_{assessment_id}.pdf"}
        )
    except AssessmentNotFoundError:
        raise
    except ValueError:
        raise AssessmentNotFoundError(assessment_id)
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}", exc_info=True)
        raise SecureVisionException("Failed to generate PDF report.", status_code=500)

@router.get("/{assessment_id}/csv")
async def get_csv_report(
    assessment_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    try:
        buffer = generate_report(assessment_id, 'csv', db, user_id)
        return Response(
            content=buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=SecureVision_Report_{assessment_id}.csv"}
        )
    except AssessmentNotFoundError:
        raise
    except ValueError:
        raise AssessmentNotFoundError(assessment_id)
    except Exception as e:
        logger.error(f"Failed to generate CSV report: {e}", exc_info=True)
        raise SecureVisionException("Failed to generate CSV report.", status_code=500)

@router.get("/{assessment_id}/json")
async def get_json_report(
    assessment_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    try:
        json_data = generate_report(assessment_id, 'json', db, user_id)
        return Response(
            content=json_data,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=SecureVision_Report_{assessment_id}.json"}
        )
    except AssessmentNotFoundError:
        raise
    except ValueError:
        raise AssessmentNotFoundError(assessment_id)
    except Exception as e:
        logger.error(f"Failed to generate JSON report: {e}", exc_info=True)
        raise SecureVisionException("Failed to generate JSON report.", status_code=500)
