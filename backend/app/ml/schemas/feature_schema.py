from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime

@dataclass
class WebsiteFeaturesV1:
    """
    Version 1 Engineered Features
    Represents raw extracted numerical and categorical features.
    """
    # SSL/TLS Features
    ssl_is_valid: bool
    cert_expiry_days: int
    tls_version: str
    
    # HTTP Header Features
    has_hsts: bool
    has_csp: bool
    has_x_frame_options: bool
    has_x_content_type_options: bool
    
    # DNS Features
    has_spf: bool
    has_dmarc: bool
    
    # WHOIS Features
    domain_age_days: int
    
    # Technology Stack
    server_software: str
    framework: str
    
    # Aggregate Scores
    ssl_score: int
    headers_score: int
    dns_score: int
    tech_score: int
    # overall_score is retained for database/dashboard telemetry, but excluded from ML classification features to prevent target leakage
    overall_score: int

@dataclass
class FeatureVector:
    """
    Structured Feature Metadata Object
    Ensures reproducibility and traceability for ML models.
    """
    assessment_id: str
    feature_schema_version: str
    created_at: str
    feature_count: int
    features: Dict[str, Any]
    label: str
    risk_class: int = -1  # Placeholder, assigned during encoding
    
    def to_dict(self):
        return {
            "assessment_id": self.assessment_id,
            "feature_schema_version": self.feature_schema_version,
            "created_at": self.created_at,
            "feature_count": self.feature_count,
            "features": self.features,
            "label": self.label,
            "risk_class": self.risk_class
        }
