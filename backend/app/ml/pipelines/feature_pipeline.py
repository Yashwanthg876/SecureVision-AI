from datetime import datetime
from dataclasses import asdict
from app.models.assessment import Assessment
from app.ml.schemas.feature_schema import WebsiteFeaturesV1, FeatureVector
from app.ml.features.ssl_features import extract_ssl_features
from app.ml.features.header_features import extract_header_features
from app.ml.features.dns_features import extract_dns_features
from app.ml.features.whois_features import extract_whois_features
from app.ml.features.technology_features import extract_technology_features

def build_feature_vector(assessment: Assessment) -> FeatureVector:
    """
    Coordinates modular feature extractors to build a complete, strongly-typed
    feature vector for a given assessment, wrapped in a metadata object.
    """
    ssl_is_valid, cert_expiry_days, tls_version = extract_ssl_features(assessment.ssl_details or {})
    has_hsts, has_csp, has_x_frame_options, has_x_content_type_options = extract_header_features(assessment.headers_details or {})
    has_spf, has_dmarc = extract_dns_features(assessment.dns_details or {})
    domain_age = extract_whois_features(assessment.whois_details or {})
    server_software, framework = extract_technology_features(assessment.technology_details or {})
    
    features = WebsiteFeaturesV1(
        ssl_is_valid=ssl_is_valid,
        cert_expiry_days=cert_expiry_days,
        tls_version=tls_version,
        has_hsts=has_hsts,
        has_csp=has_csp,
        has_x_frame_options=has_x_frame_options,
        has_x_content_type_options=has_x_content_type_options,
        has_spf=has_spf,
        has_dmarc=has_dmarc,
        domain_age_days=domain_age,
        server_software=server_software,
        framework=framework,
        ssl_score=assessment.ssl_score,
        headers_score=assessment.headers_score,
        dns_score=assessment.dns_score,
        tech_score=assessment.tech_score,
        overall_score=assessment.overall_score,
    )
    
    features_dict = asdict(features)
    
    return FeatureVector(
        assessment_id=str(assessment.id),
        feature_schema_version="1.0",
        created_at=datetime.utcnow().isoformat(),
        feature_count=len(features_dict),
        features=features_dict,
        label=assessment.risk_level
    )
