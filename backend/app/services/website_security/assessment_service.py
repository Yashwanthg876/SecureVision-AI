import asyncio
import time
import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.website_security import AssessmentResponse
from app.models.assessment import Assessment, AssessmentFinding
from app.models.user import User
from .url_validator import validate_url
from .ssl_service import analyze_ssl
from .headers_service import analyze_headers
from .dns_service import analyze_dns
from .whois_service import analyze_whois
from .technology_service import analyze_technology
from .scoring_service import calculate_score
from .recommendation_service import generate_recommendations
from app.repositories.assessment_repository import assessment_repository
from app.core.exceptions import AssessmentNotFoundError, SecureVisionException

def _resolve_user_id_for_assessment(db: Session, user_id: Any) -> uuid.UUID:
    if isinstance(user_id, uuid.UUID):
        return user_id
    if isinstance(user_id, str) and user_id and user_id != "guest_user":
        try:
            return uuid.UUID(user_id)
        except Exception:
            pass
    raise SecureVisionException("Authentication is required.", 401)

async def perform_assessment(target_url: str, db: Session, user_id: Any) -> AssessmentResponse:
    """
    Orchestrates the entire website security assessment pipeline asynchronously.
    Persists the result to the database and returns the AssessmentResponse.
    """
    start_time = time.time()
    resolved_user_id = _resolve_user_id_for_assessment(db, user_id)
    
    # 1. Validate and clean URL
    hostname, clean_url = validate_url(target_url)
    
    # 2. Run independent services concurrently where possible
    ssl_task = asyncio.to_thread(analyze_ssl, hostname)
    dns_task = analyze_dns(hostname)
    whois_task = analyze_whois(hostname)
    headers_task = analyze_headers(clean_url)
    tech_task = analyze_technology(clean_url)
    
    ssl_info, dns_info, whois_info, headers_info, tech_info = await asyncio.gather(
        ssl_task, dns_task, whois_task, headers_task, tech_task, return_exceptions=False
    )
    
    # 3. Calculate Score and Recommendations
    scores = calculate_score(ssl_info, headers_info, dns_info, whois_info, tech_info)
    recommendations = generate_recommendations(ssl_info, headers_info, dns_info, whois_info, tech_info)
    
    scan_duration = int((time.time() - start_time) * 1000)
    
    # 4. Count severities
    critical_count = sum(1 for r in recommendations if r.severity == "Critical")
    high_count = sum(1 for r in recommendations if r.severity == "High")
    medium_count = sum(1 for r in recommendations if r.severity == "Medium")
    low_count = sum(1 for r in recommendations if r.severity == "Low")
    
    # 5. Build entities
    db_assessment = Assessment( # type: ignore
        user_id=resolved_user_id,
        target_url=clean_url,
        domain=hostname,
        assessment_type="Passive",
        overall_score=scores["overall_score"],
        risk_level=scores["risk_level"],
        ssl_score=scores["ssl_score"],
        headers_score=scores["headers_score"],
        dns_score=scores["dns_score"],
        tech_score=scores["tech_score"],
        recommendation_count=len(recommendations),
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        scan_duration=scan_duration,
        status="Completed",
        engine_version="1.0",
        ssl_details=ssl_info.model_dump(),
        headers_details=headers_info.model_dump(),
        dns_details=dns_info.model_dump(),
        whois_details=whois_info.model_dump(),
        technology_details=tech_info.model_dump()
    )
    
    db_findings = []
    for rec in recommendations:
        db_finding = AssessmentFinding( # type: ignore
            category=rec.category,
            title=rec.title,
            description=rec.description,
            severity=rec.severity,
            recommendation=rec.recommendation,
            reference=rec.reference
        )
        db_findings.append(db_finding)
    db_assessment = assessment_repository.save_assessment_with_findings(db, db_assessment, db_findings)
    
    return AssessmentResponse(
        id=str(db_assessment.id),
        target_url=db_assessment.target_url,
        domain=db_assessment.domain,
        overall_score=db_assessment.overall_score,
        risk_level=db_assessment.risk_level,
        ssl_score=db_assessment.ssl_score,
        headers_score=db_assessment.headers_score,
        dns_score=db_assessment.dns_score,
        tech_score=db_assessment.tech_score,
        recommendation_count=db_assessment.recommendation_count,
        critical_count=db_assessment.critical_count,
        high_count=db_assessment.high_count,
        medium_count=db_assessment.medium_count,
        low_count=db_assessment.low_count,
        scan_duration=db_assessment.scan_duration,
        status=db_assessment.status,
        ssl_tls=ssl_info,
        http_headers=headers_info,
        dns=dns_info,
        whois=whois_info,
        technology=tech_info,
        recommendations=recommendations,
        created_at=db_assessment.created_at.isoformat()
    )

def get_assessment_history(db: Session, user_id: Any, domain: str = None, risk_level: str = None, status: str = None):
    assessments = assessment_repository.get_user_assessments(db, user_id, domain, risk_level, status)
    return [
        {
            "id": str(a.id),
            "domain": a.domain,
            "overall_score": a.overall_score,
            "risk_level": a.risk_level,
            "scan_duration": a.scan_duration,
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else ""
        } for a in assessments
    ]

def get_assessment_timeline(db: Session, user_id: Any):
    assessments = assessment_repository.get_timeline(db, user_id)
    return [
        {
            "date": a.created_at.strftime("%Y-%m-%d") if a.created_at else "",
            "score": a.overall_score,
            "domain": a.domain
        } for a in assessments
    ]

def compare_assessments(db: Session, user_id: Any, id1: str = None, id2: str = None, domain: str = None):
    if id1 and id2:
        a1 = assessment_repository.get(db, id1)
        a2 = assessment_repository.get(db, id2)
    elif domain:
        assessments = assessment_repository.get_latest_two_by_domain(db, user_id, domain)
        if len(assessments) < 2:
            raise SecureVisionException("Not enough history to compare for this domain.", 400)
        a1, a2 = assessments[1], assessments[0] # Older, Newer
    else:
        raise SecureVisionException("Must provide either id1 and id2, or a domain.", 400)

    if not a1 or not a2:
        raise AssessmentNotFoundError("One or both assessments not found")
    resolved_user_id = _resolve_user_id_for_assessment(db, user_id)
    if a1.user_id != resolved_user_id or a2.user_id != resolved_user_id:
        raise AssessmentNotFoundError("One or both assessments not found")
        
    f1 = assessment_repository.get_findings_by_assessment_id(db, str(a1.id))
    f2 = assessment_repository.get_findings_by_assessment_id(db, str(a2.id))
    
    f1_titles = set([f.title for f in f1])
    f2_titles = set([f.title for f in f2])
    
    return {
        "assessment_old": {"id": str(a1.id), "date": a1.created_at.isoformat() if a1.created_at else "", "score": a1.overall_score},
        "assessment_new": {"id": str(a2.id), "date": a2.created_at.isoformat() if a2.created_at else "", "score": a2.overall_score},
        "score_delta": a2.overall_score - a1.overall_score,
        "resolved_findings": list(f1_titles - f2_titles),
        "new_findings": list(f2_titles - f1_titles),
        "persistent_findings": list(f1_titles.intersection(f2_titles))
    }

def get_assessment_by_id(db: Session, user_id: Any, id: str):
    assessment = assessment_repository.get(db, id)
    resolved_user_id = _resolve_user_id_for_assessment(db, user_id)
    if not assessment or assessment.is_deleted or assessment.user_id != resolved_user_id:
        raise AssessmentNotFoundError(id)
        
    findings = assessment_repository.get_findings_by_assessment_id(db, str(assessment.id))
    
    return {
        "id": str(assessment.id),
        "target_url": assessment.target_url,
        "domain": assessment.domain,
        "overall_score": assessment.overall_score,
        "risk_level": assessment.risk_level,
        "ssl_score": assessment.ssl_score,
        "headers_score": assessment.headers_score,
        "dns_score": assessment.dns_score,
        "tech_score": assessment.tech_score,
        "recommendation_count": assessment.recommendation_count,
        "critical_count": assessment.critical_count,
        "high_count": assessment.high_count,
        "medium_count": assessment.medium_count,
        "low_count": assessment.low_count,
        "scan_duration": assessment.scan_duration,
        "status": assessment.status,
        "ssl_tls": assessment.ssl_details,
        "http_headers": assessment.headers_details,
        "dns": assessment.dns_details,
        "whois": assessment.whois_details,
        "technology": assessment.technology_details,
        "recommendations": [
            {
                "category": f.category,
                "title": f.title,
                "description": f.description,
                "severity": f.severity,
                "recommendation": f.recommendation,
                "reference": f.reference
            } for f in findings
        ],
        "created_at": assessment.created_at.isoformat() if assessment.created_at else ""
    }
