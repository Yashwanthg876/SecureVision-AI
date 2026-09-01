import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.assessment_repository import assessment_repository
from app.core.exceptions import AssessmentNotFoundError
from .pdf_generator import generate_pdf_report
from .csv_exporter import generate_csv_report
from .json_exporter import generate_json_report
from .report_builder import ReportBuilder, NormalizedReportModel

class ReportGeneratorFactory:
    """
    Factory pattern to generate reports. Easily extensible for future compliance reports.
    """
    @staticmethod
    def get_generator(format_type: str, compliance_framework: str = None):
        if format_type == 'pdf':
            return generate_pdf_report
        elif format_type == 'csv':
            return generate_csv_report
        elif format_type == 'json':
            return generate_json_report
        else:
            raise ValueError(f"Unsupported report format: {format_type}")

def generate_report(assessment_id: str, format_type: str, db: Session, user_id: Any = None):
    """
    Fetches assessment data from the database and routes to the appropriate report generator.
    """
    assessment = assessment_repository.get(db, assessment_id)
    
    if not assessment or assessment.is_deleted:
        raise AssessmentNotFoundError(assessment_id)
    try:
        resolved_user_id = user_id if isinstance(user_id, uuid.UUID) else uuid.UUID(str(user_id))
    except (TypeError, ValueError):
        raise AssessmentNotFoundError(assessment_id)
    if assessment.user_id != resolved_user_id:
        raise AssessmentNotFoundError(assessment_id)
        
    findings = assessment_repository.get_findings_by_assessment_id(db, assessment_id)
    
    # Retrieve user info if available
    from app.models.user import User
    user = None
    if user_id:
        if isinstance(user_id, uuid.UUID):
            user = db.query(User).filter(User.id == user_id).first()
        elif isinstance(user_id, str) and user_id != "guest_user":
            try:
                user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
            except Exception:
                pass
    if not user:
        raise AssessmentNotFoundError(assessment_id)

    normalized_report = ReportBuilder(assessment, findings, user=user).build()
    
    generator = ReportGeneratorFactory.get_generator(format_type)
    return generator(normalized_report)

def list_user_reports(db: Session, user_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves all available security reports for the specified user or guest account.
    """
    assessments = assessment_repository.get_user_assessments(db, user_id=user_id)
    
    reports_list = []
    for asm in assessments:
        findings = assessment_repository.get_findings_by_assessment_id(db, str(asm.id))
        reports_list.append({
            "id": str(asm.id),
            "title": f"Security Assessment Report - {asm.domain}",
            "target_domain": asm.domain,
            "target_url": asm.target_url,
            "overall_score": asm.overall_score,
            "risk_level": asm.risk_level,
            "total_findings": len(findings),
            "report_type": "Comprehensive Audit",
            "created_at": asm.created_at.isoformat() if asm.created_at else "",
            "formats": ["pdf", "csv", "json"]
        })
        
    return reports_list
