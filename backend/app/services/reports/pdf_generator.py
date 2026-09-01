import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from .report_builder import NormalizedReportModel

def generate_pdf_report(report: NormalizedReportModel) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Title'], fontSize=28, textColor=colors.HexColor("#1e3a8a"), spaceAfter=20, alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor("#475569"), spaceAfter=40, alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'SectionHeading', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1e40af"), spaceBefore=20, spaceAfter=10, borderPadding=10, borderBottomWidth=1, borderColor=colors.HexColor("#e2e8f0")
    )
    subheading_style = ParagraphStyle(
        'SubHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#334155"), spaceBefore=15, spaceAfter=5
    )
    normal_style = styles['Normal']
    
    story = []
    
    # --- COVER PAGE ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>SecureVision AI</b>", title_style))
    story.append(Paragraph("Comprehensive Security Assessment Report", subtitle_style))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"<b>Target Domain:</b> {report.domain}", normal_style))
    story.append(Paragraph(f"<b>Target URL:</b> {report.target_url}", normal_style))
    story.append(Paragraph(f"<b>Assessment Date:</b> {report.assessment_date.strftime('%Y-%m-%d %H:%M:%S UTC')}", normal_style))
    story.append(Paragraph(f"<b>Auditor / Analyst:</b> {report.auditor_name} ({report.user_role})", normal_style))
    story.append(Paragraph(f"<b>Organization:</b> {report.organization}", normal_style))
    story.append(Paragraph(f"<b>Account Email:</b> {report.user_email}", normal_style))
    story.append(Paragraph(f"<b>Report Classification:</b> CONFIDENTIAL / RESTRICTED", normal_style))
    
    story.append(Spacer(1, 60))
    
    # Overall Score Box
    score_color = colors.HexColor("#22c55e") if report.overall_score >= 90 else colors.HexColor("#eab308") if report.overall_score >= 70 else colors.HexColor("#ef4444")
    
    score_data = [
        ["Overall Security Score", "Risk Level"],
        [f"{report.overall_score} / 100", report.risk_level]
    ]
    score_table = Table(score_data, colWidths=[250, 150])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#f8fafc")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor("#475569")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (0, 1), score_color),
        ('TEXTCOLOR', (1, 1), (1, 1), score_color),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 18),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0"))
    ]))
    
    story.append(score_table)
    story.append(PageBreak())
    
    # --- EXECUTIVE SUMMARY ---
    story.append(Paragraph("Executive Summary", heading_style))
    exec_summary_text = (
        f"This report presents the findings of a passive security assessment conducted on <b>{report.domain}</b>. "
        f"The assessment yielded an overall security score of <b>{report.overall_score}/100</b>, which places the target in the "
        f"<b>{report.risk_level}</b> risk category. A total of <b>{report.total_findings}</b> issues were identified, "
        f"including {report.critical_count} critical, {report.high_count} high, {report.medium_count} medium, and {report.low_count} low severity findings."
    )
    story.append(Paragraph(exec_summary_text, normal_style))
    story.append(Spacer(1, 20))
    
    # Category Breakdowns
    story.append(Paragraph("Category Score Breakdown", subheading_style))
    cat_data = [
        ["Category", "Score"],
        ["SSL/TLS Configuration", f"{report.ssl_score}/100"],
        ["HTTP Security Headers", f"{report.headers_score}/100"],
        ["DNS Configuration", f"{report.dns_score}/100"],
        ["Technology Stack", f"{report.tech_score}/100"]
    ]
    cat_table = Table(cat_data, colWidths=[250, 150])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
    ]))
    story.append(cat_table)
    story.append(PageBreak())
    
    # --- DETAILED FINDINGS ---
    story.append(Paragraph("Detailed Security Findings", heading_style))
    
    if not report.findings:
        story.append(Paragraph("No security vulnerabilities were identified during this assessment.", normal_style))
    else:
        for finding in sorted(report.findings, key=lambda x: ['Critical', 'High', 'Medium', 'Low'].index(x.severity) if x.severity in ['Critical', 'High', 'Medium', 'Low'] else 99):
            
            sev_color = "#ef4444" if finding.severity == "Critical" else "#f97316" if finding.severity == "High" else "#eab308" if finding.severity == "Medium" else "#3b82f6"
            
            story.append(Paragraph(f"<b>{finding.title}</b>", subheading_style))
            
            finding_data = [
                [Paragraph("<b>Category:</b>", normal_style), Paragraph(finding.category, normal_style)],
                [Paragraph("<b>Severity:</b>", normal_style), Paragraph(f'<font color="{sev_color}">{finding.severity}</font>', normal_style)],
                [Paragraph("<b>Description:</b>", normal_style), Paragraph(finding.description, normal_style)],
                [Paragraph("<b>Recommendation:</b>", normal_style), Paragraph(finding.recommendation, normal_style)],
                [Paragraph("<b>Reference:</b>", normal_style), Paragraph(finding.reference or "N/A", normal_style)]
            ]
            
            t = Table(finding_data, colWidths=[100, 350])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f8fafc")),
            ]))
            story.append(t)
            story.append(Spacer(1, 20))
            
    # Add footer (reportlab doc template handles pages, but we'll just add it to the end of story for now)
    story.append(PageBreak())
    story.append(Spacer(1, 300))
    story.append(Paragraph("<b>Generated by SecureVision AI</b>", ParagraphStyle('Footer', alignment=TA_CENTER, textColor=colors.HexColor("#64748b"))))
    story.append(Paragraph(f"Assessment Engine Version: {report.engine_version} | Report Version: {report.report_version}", ParagraphStyle('Footer2', alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#94a3b8"))))
    story.append(Paragraph(f"Assessment ID: {report.assessment_id}", ParagraphStyle('Footer3', alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#94a3b8"))))

    doc.build(story)
    
    buffer.seek(0)
    return buffer
