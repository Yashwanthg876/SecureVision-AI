from pydantic import BaseModel, Field
from typing import List, Optional

class ThreatIOCResponse(BaseModel):
    id: str
    ioc_value: str
    ioc_type: str
    threat_type: str
    severity: str
    confidence_score: float
    source: str
    target_sector: str
    description: Optional[str] = None
    recommended_action: Optional[str] = None
    status: str
    country_code: Optional[str] = "US"
    created_at: str

class IOCLookupRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2048, description="IP, Domain, File Hash, URL, or CVE ID to search")

class IOCLookupResponse(BaseModel):
    query: str
    matched: bool
    ioc: Optional[ThreatIOCResponse] = None
    risk_level: str
    verdict: str
    reputation_score: float
    analysis_details: str
    recommended_action: str

class ThreatIntelStatsResponse(BaseModel):
    total_active_iocs: int
    critical_threats: int
    high_threats: int
    medium_threats: int
    low_threats: int
    top_threat_vector: str
    avg_confidence_score: float
    category_distribution: dict
