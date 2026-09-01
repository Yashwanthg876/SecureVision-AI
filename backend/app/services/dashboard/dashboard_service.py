import uuid
from datetime import datetime, timedelta
from typing import List, Any, Optional
from sqlalchemy.orm import Session

from app.models.assessment import Assessment, AssessmentFinding
from app.models.github_scan import GitHubScan
from app.models.ai_detection_scan import AIDetectionScan
from app.repositories.assessment_repository import assessment_repository
from app.schemas.dashboard import (
    SummaryKPI,
    ThreatTrendDataPoint,
    RiskDistribution,
    RecentActivity,
    CriticalFinding
)

def _get_user_identifiers(db: Session, user_id: Any) -> tuple[Optional[uuid.UUID], str]:
    resolved_uuid = None
    if isinstance(user_id, uuid.UUID):
        resolved_uuid = user_id
    elif isinstance(user_id, str) and user_id:
        try:
            resolved_uuid = uuid.UUID(user_id)
        except Exception:
            pass

    user_str = str(resolved_uuid) if resolved_uuid else ""
    return resolved_uuid, user_str

class DashboardService:
    def get_summary(self, db: Session, user_id: Any) -> SummaryKPI:
        """
        Aggregate genuine KPI statistics directly from database records.
        """
        today = datetime.utcnow().date()
        user_uuid, user_str = _get_user_identifiers(db, user_id)

        # 1. Website Assessments
        asm_query = db.query(Assessment).filter(Assessment.is_deleted == False)
        asm_query = asm_query.filter(Assessment.user_id == user_uuid)
        assessments = asm_query.all()

        websites_total = len(assessments)
        websites_scanned_today = sum(1 for a in assessments if a.created_at and a.created_at.date() == today)

        # 2. GitHub Security Scans
        gh_query = db.query(GitHubScan).filter(GitHubScan.user_id == user_str)
        github_scans = gh_query.all()
        repos_total = len(github_scans)
        repos_high_risk = sum(1 for g in github_scans if g.risk_level in ["High", "Critical"])

        # 3. AI Detection Scans
        ai_query = db.query(AIDetectionScan).filter(AIDetectionScan.user_id == user_str)
        ai_scans = ai_query.all()
        ai_threats_total = len(ai_scans)
        ai_threats_critical = sum(1 for a in ai_scans if a.risk_level in ["Critical", "High"])

        # Calculate genuine overall security score
        all_scores = [a.overall_score for a in assessments] + [g.security_score for g in github_scans]
        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)
            if avg_score >= 90:
                score_status = "Healthy"
            elif avg_score >= 70:
                score_status = "Fair"
            elif avg_score >= 40:
                score_status = "Warning"
            else:
                score_status = "Critical"
        else:
            avg_score = 0
            score_status = "No Data"

        return SummaryKPI(
            score=int(avg_score),
            score_status=score_status,
            score_trend="0%",
            websites_total=websites_total,
            websites_scanned_today=websites_scanned_today,
            repos_total=repos_total,
            repos_high_risk=repos_high_risk,
            ai_threats_total=ai_threats_total,
            ai_threats_critical=ai_threats_critical,
        )

    def get_threat_trend(self, db: Session, user_id: Any, days: int = 7) -> List[ThreatTrendDataPoint]:
        """
        Compute daily threat finding counts for the line chart using real user scan timestamps.
        """
        user_uuid, user_str = _get_user_identifiers(db, user_id)
        cutoff = datetime.utcnow() - timedelta(days=days)
        trend_map = {}
        for i in range(days + 1):
            date_str = (cutoff + timedelta(days=i)).strftime("%Y-%m-%d")
            trend_map[date_str] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

        # Website Assessment findings
        asm_query = db.query(Assessment).filter(Assessment.created_at >= cutoff, Assessment.is_deleted == False)
        asm_query = asm_query.filter(Assessment.user_id == user_uuid)
        assessments = asm_query.all()
        for a in assessments:
            if a.created_at:
                d_str = a.created_at.strftime("%Y-%m-%d")
                if d_str in trend_map:
                    sev = a.risk_level.capitalize() if a.risk_level else "Low"
                    if sev in trend_map[d_str]:
                        trend_map[d_str][sev] += 1

        # GitHub Scans
        gh_query = db.query(GitHubScan).filter(
            GitHubScan.created_at >= cutoff,
            GitHubScan.user_id == user_str
        )
        github_scans = gh_query.all()
        for g in github_scans:
            if g.created_at:
                d_str = g.created_at.strftime("%Y-%m-%d")
                if d_str in trend_map:
                    trend_map[d_str]["Critical"] += g.critical_count
                    trend_map[d_str]["High"] += g.high_count
                    trend_map[d_str]["Medium"] += g.medium_count
                    trend_map[d_str]["Low"] += g.low_count

        # AI Detection Scans
        ai_query = db.query(AIDetectionScan).filter(
            AIDetectionScan.created_at >= cutoff,
            AIDetectionScan.user_id == user_str
        )
        ai_scans = ai_query.all()
        for ai in ai_scans:
            if ai.created_at:
                d_str = ai.created_at.strftime("%Y-%m-%d")
                if d_str in trend_map:
                    sev = ai.risk_level.capitalize() if ai.risk_level else "Low"
                    if sev in trend_map[d_str]:
                        trend_map[d_str][sev] += 1

        return [
            ThreatTrendDataPoint(
                date=k,
                Critical=v["Critical"],
                High=v["High"],
                Medium=v["Medium"],
                Low=v["Low"],
            )
            for k, v in sorted(trend_map.items())
        ]

    def get_risk_distribution(self, db: Session, user_id: Any) -> List[RiskDistribution]:
        """
        Aggregate real risk levels across all completed user scans.
        """
        user_uuid, user_str = _get_user_identifiers(db, user_id)
        counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        colors = {"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308", "Low": "#3b82f6"}

        asm_query = db.query(Assessment).filter(Assessment.is_deleted == False)
        asm_query = asm_query.filter(Assessment.user_id == user_uuid)
        assessments = asm_query.all()
        for a in assessments:
            sev = a.risk_level.capitalize() if a.risk_level else "Low"
            if sev in counts:
                counts[sev] += 1

        gh_query = db.query(GitHubScan).filter(GitHubScan.user_id == user_str)
        github_scans = gh_query.all()
        for g in github_scans:
            counts["Critical"] += g.critical_count
            counts["High"] += g.high_count
            counts["Medium"] += g.medium_count
            counts["Low"] += g.low_count

        ai_query = db.query(AIDetectionScan).filter(AIDetectionScan.user_id == user_str)
        ai_scans = ai_query.all()
        for ai in ai_scans:
            sev = ai.risk_level.capitalize() if ai.risk_level else "Low"
            if sev in counts:
                counts[sev] += 1

        return [
            RiskDistribution(name=k, value=v, color=colors[k])
            for k, v in counts.items()
        ]

    def get_recent_activity(self, db: Session, user_id: Any) -> List[RecentActivity]:
        """
        Merge and sort recent activities across Website, GitHub, and AI Detection modules.
        """
        user_uuid, user_str = _get_user_identifiers(db, user_id)
        events = []

        # Website Security
        asm_query = db.query(Assessment).filter(Assessment.is_deleted == False)
        asm_query = asm_query.filter(Assessment.user_id == user_uuid)
        assessments = asm_query.all()
        for a in assessments:
            if a.created_at:
                events.append(
                    RecentActivity(
                        id=f"web-{a.id}",
                        time=a.created_at,
                        module="Website Security",
                        action=f"Website Scan Completed ({a.domain})",
                        status="Success" if a.status == "Completed" else "Failed",
                    )
                )

        # GitHub Security
        gh_query = db.query(GitHubScan).filter(GitHubScan.user_id == user_str)
        github_scans = gh_query.all()
        for g in github_scans:
            if g.created_at:
                events.append(
                    RecentActivity(
                        id=f"gh-{g.id}",
                        time=g.created_at,
                        module="GitHub Security",
                        action=f"Secret & Vulnerability Scan ({g.repo_name})",
                        status="Success" if g.status == "Completed" else "Failed",
                    )
                )

        # AI Detection
        ai_query = db.query(AIDetectionScan).filter(AIDetectionScan.user_id == user_str)
        ai_scans = ai_query.all()
        for ai in ai_scans:
            if ai.created_at:
                events.append(
                    RecentActivity(
                        id=f"ai-{ai.id}",
                        time=ai.created_at,
                        module="AI Detection",
                        action=f"AI Content & Code Scan ({ai.content_type})",
                        status="Success" if ai.status == "Completed" else "Failed",
                    )
                )

        # Sort by most recent timestamp
        events.sort(key=lambda x: x.time, reverse=True)
        return events[:10]

    def get_critical_findings(self, db: Session, user_id: Any) -> List[CriticalFinding]:
        """
        Retrieve genuine critical and high findings from user scans.
        """
        user_uuid, user_str = _get_user_identifiers(db, user_id)
        findings = []

        # Website findings
        asm_query = db.query(Assessment).filter(Assessment.is_deleted == False)
        asm_query = asm_query.filter(Assessment.user_id == user_uuid)
        assessments = asm_query.all()
        for a in assessments:
            a_findings = assessment_repository.get_findings_by_assessment_id(db, a.id)
            for f in a_findings:
                if f.severity in ["Critical", "High"]:
                    findings.append(
                        CriticalFinding(
                            id=f"finding-{f.id}",
                            severity=f.severity,
                            module="Website Security",
                            description=f"{a.domain}: {f.title}",
                            timestamp=f.created_at or a.created_at,
                        )
                    )

        # GitHub findings
        gh_query = db.query(GitHubScan).filter(GitHubScan.user_id == user_str)
        github_scans = gh_query.all()
        for g in github_scans:
            if g.critical_count > 0 or g.high_count > 0:
                findings.append(
                    CriticalFinding(
                        id=f"gh-finding-{g.id}",
                        severity="Critical" if g.critical_count > 0 else "High",
                        module="GitHub Security",
                        description=f"{g.repo_name}: {g.critical_count + g.high_count} secrets/vulnerabilities detected",
                        timestamp=g.created_at,
                    )
                )

        findings.sort(key=lambda x: x.timestamp, reverse=True)
        return findings[:10]

dashboard_service = DashboardService()
