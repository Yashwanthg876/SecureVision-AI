import json
from .report_builder import NormalizedReportModel

def generate_json_report(report: NormalizedReportModel) -> str:
    
    # Structure into logical sections
    report_dict = {
        "metadata": {
            "assessment_id": report.assessment_id,
            "target": {
                "domain": report.domain,
                "url": report.target_url
            },
            "date": report.assessment_date.isoformat(),
            "engine_version": report.engine_version,
            "report_version": report.report_version,
            "duration_ms": report.scan_duration_ms
        },
        "executive_summary": {
            "overall_score": report.overall_score,
            "risk_level": report.risk_level,
            "status": report.status,
            "category_scores": {
                "ssl_tls": report.ssl_score,
                "http_headers": report.headers_score,
                "dns": report.dns_score,
                "technology_stack": report.tech_score
            },
            "findings_summary": {
                "total": report.total_findings,
                "critical": report.critical_count,
                "high": report.high_count,
                "medium": report.medium_count,
                "low": report.low_count
            }
        },
        "telemetry_data": {
            "ssl_tls": report.telemetry_ssl_tls,
            "http_headers": report.telemetry_http_headers,
            "dns": report.telemetry_dns,
            "whois": report.telemetry_whois,
            "technology_stack": report.telemetry_technology
        },
        "findings": [
            {
                "category": f.category,
                "title": f.title,
                "severity": f.severity,
                "description": f.description,
                "recommendation": f.recommendation,
                "reference": f.reference
            } for f in report.findings
        ]
    }
    
    return json.dumps(report_dict, indent=2)
