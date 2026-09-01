from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SummaryKPI(BaseModel):
    score: int
    score_status: str
    score_trend: str
    websites_total: int
    websites_scanned_today: int
    repos_total: int
    repos_high_risk: int
    ai_threats_total: int
    ai_threats_critical: int

class ThreatTrendDataPoint(BaseModel):
    date: str
    Critical: int
    High: int
    Medium: int
    Low: int

class RiskDistribution(BaseModel):
    name: str
    value: int
    color: str

class RecentActivity(BaseModel):
    id: str
    time: datetime
    module: str
    action: str
    status: str

class CriticalFinding(BaseModel):
    id: str
    severity: str
    module: str
    description: str
    timestamp: datetime
