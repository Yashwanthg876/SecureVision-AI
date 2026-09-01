import io
import csv
from .report_builder import NormalizedReportModel

def generate_csv_report(report: NormalizedReportModel) -> io.StringIO:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Headers
    writer.writerow([
        "Assessment ID",
        "Domain",
        "Target URL",
        "Assessment Date",
        "Overall Score",
        "Risk Level",
        "Status",
        "Finding Category",
        "Severity",
        "Finding Title",
        "Description",
        "Recommendation",
        "Reference"
    ])
    
    for finding in report.findings:
        writer.writerow([
            report.assessment_id,
            report.domain,
            report.target_url,
            report.assessment_date.strftime("%Y-%m-%d %H:%M:%S UTC"),
            report.overall_score,
            report.risk_level,
            report.status,
            finding.category,
            finding.severity,
            finding.title,
            finding.description,
            finding.recommendation,
            finding.reference or ""
        ])
        
    buffer.seek(0)
    return buffer
