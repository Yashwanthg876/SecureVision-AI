from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class FindingReportModel:
    category: str
    title: str
    severity: str
    description: str
    recommendation: str
    reference: Optional[str]

@dataclass
class NormalizedReportModel:
    # Metadata
    assessment_id: str
    domain: str
    target_url: str
    assessment_date: datetime
    engine_version: str
    report_version: str
    scan_duration_ms: float
    status: str
    
    # Executive Summary / Scores
    overall_score: int
    risk_level: str
    
    # Category Scores
    ssl_score: int
    headers_score: int
    dns_score: int
    tech_score: int
    
    # Finding Summary
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    
    # Raw Telemetry Data (Dictionaries)
    telemetry_ssl_tls: Dict[str, Any]
    telemetry_http_headers: Dict[str, Any]
    telemetry_dns: Dict[str, Any]
    telemetry_whois: Dict[str, Any]
    telemetry_technology: Dict[str, Any]
    
    # User & Organization Context
    auditor_name: str = "Security Analyst"
    user_email: str = "admin@securevision.ai"
    organization: str = "SecureVision AI Enterprise"
    user_role: str = "Security Auditor"
    
    # Detailed Findings
    findings: List[FindingReportModel] = None

class ReportBuilder:
    """
    Transforms raw database Assessment and AssessmentFinding models into a normalized
    Report Model that can be universally consumed by any export generator (PDF, CSV, JSON, etc).
    """
    def __init__(self, assessment, findings, user=None):
        self.assessment = assessment
        self.findings = findings
        self.user = user
        
    def build(self) -> NormalizedReportModel:
        mapped_findings = [
            FindingReportModel(
                category=f.category,
                title=f.title,
                severity=f.severity,
                description=f.description,
                recommendation=f.recommendation,
                reference=f.reference
            ) for f in self.findings
        ]
        
        auditor_name = self.user.full_name if self.user and hasattr(self.user, 'full_name') and self.user.full_name else (self.assessment.user.full_name if getattr(self.assessment, 'user', None) and self.assessment.user.full_name else "PRAKASH")
        user_email = self.user.email if self.user and hasattr(self.user, 'email') and self.user.email else (self.assessment.user.email if getattr(self.assessment, 'user', None) and self.assessment.user.email else "9924008052@klu.ac.in")
        organization = self.user.organization if self.user and hasattr(self.user, 'organization') and self.user.organization else (self.assessment.user.organization if getattr(self.assessment, 'user', None) and self.assessment.user.organization else "KLU Cyber Security")
        user_role = self.user.role if self.user and hasattr(self.user, 'role') and self.user.role else "Lead Security Analyst"

        return NormalizedReportModel(
            assessment_id=str(self.assessment.id),
            domain=self.assessment.domain,
            target_url=self.assessment.target_url,
            assessment_date=self.assessment.created_at or datetime.utcnow(),
            engine_version=self.assessment.engine_version or "1.0",
            report_version="1.0",
            scan_duration_ms=self.assessment.scan_duration or 0,
            status=self.assessment.status or "Completed",
            overall_score=self.assessment.overall_score or 0,
            risk_level=self.assessment.risk_level or "Low",
            ssl_score=self.assessment.ssl_score or 100,
            headers_score=self.assessment.headers_score or 100,
            dns_score=self.assessment.dns_score or 100,
            tech_score=self.assessment.tech_score or 100,
            total_findings=self.assessment.recommendation_count or len(mapped_findings),
            critical_count=self.assessment.critical_count or 0,
            high_count=self.assessment.high_count or 0,
            medium_count=self.assessment.medium_count or 0,
            low_count=self.assessment.low_count or 0,
            telemetry_ssl_tls=self.assessment.ssl_details or {},
            telemetry_http_headers=self.assessment.headers_details or {},
            telemetry_dns=self.assessment.dns_details or {},
            telemetry_whois=self.assessment.whois_details or {},
            telemetry_technology=self.assessment.technology_details or {},
            auditor_name=auditor_name,
            user_email=user_email,
            organization=organization,
            user_role=user_role,
            findings=mapped_findings
        )
