from pydantic import BaseModel, Field
from typing import List, Optional

class SSLInfo(BaseModel):
    is_valid: bool
    issuer: str
    subject: str
    expires_in_days: int
    protocol: str
    error: Optional[str] = None

class HTTPHeadersInfo(BaseModel):
    strict_transport_security: bool
    content_security_policy: bool
    x_frame_options: bool
    x_content_type_options: bool
    missing_headers: List[str]

class DNSInfo(BaseModel):
    a_records: List[str]
    mx_records: List[str]
    txt_records: List[str]
    has_spf: bool
    has_dmarc: bool

class WHOISInfo(BaseModel):
    registrar: str
    creation_date: Optional[str]
    expiration_date: Optional[str]
    days_until_expiration: Optional[int]

class TechnologyInfo(BaseModel):
    server: Optional[str]
    frameworks: List[str]
    x_powered_by: Optional[str]

class Recommendation(BaseModel):
    category: str
    title: str
    description: str
    severity: str
    recommendation: str
    reference: Optional[str] = None

class AssessmentResponse(BaseModel):
    id: str
    target_url: str
    domain: str
    overall_score: int
    risk_level: str
    ssl_score: int
    headers_score: int
    dns_score: int
    tech_score: int
    recommendation_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    scan_duration: int
    status: str
    ssl_tls: SSLInfo
    http_headers: HTTPHeadersInfo
    dns: DNSInfo
    whois: WHOISInfo
    technology: TechnologyInfo
    recommendations: List[Recommendation]
    created_at: str

class AssessmentRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)
