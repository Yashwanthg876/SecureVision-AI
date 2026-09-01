from typing import Dict, Any
from app.schemas.website_security import (
    SSLInfo, HTTPHeadersInfo, DNSInfo, WHOISInfo, TechnologyInfo
)

def calculate_score(
    ssl_info: SSLInfo,
    headers_info: HTTPHeadersInfo,
    dns_info: DNSInfo,
    whois_info: WHOISInfo,
    tech_info: TechnologyInfo
) -> Dict[str, Any]:
    """
    Deterministically calculates security scores and risk level based on standard heuristics.
    Returns sub-scores and overall risk level.
    """
    ssl_score = 100
    headers_score = 100
    dns_score = 100
    tech_score = 100
    
    # 1. SSL Penalties
    if not ssl_info.is_valid:
        ssl_score -= 100
    elif ssl_info.expires_in_days is not None and ssl_info.expires_in_days < 30:
        ssl_score -= 40
        
    # 2. Header Penalties
    if not headers_info.strict_transport_security:
        headers_score -= 30
    if not headers_info.content_security_policy:
        headers_score -= 30
    if not headers_info.x_frame_options:
        headers_score -= 20
    if not headers_info.x_content_type_options:
        headers_score -= 20
        
    # 3. DNS Penalties
    if not dns_info.has_spf:
        dns_score -= 50
    if not dns_info.has_dmarc:
        dns_score -= 50
        
    # 4. Tech/Information Disclosure Penalties
    if tech_info.server:
        tech_score -= 25
    if tech_info.x_powered_by:
        tech_score -= 25
        
    # Bounds check sub-scores
    ssl_score = max(0, min(100, ssl_score))
    headers_score = max(0, min(100, headers_score))
    dns_score = max(0, min(100, dns_score))
    tech_score = max(0, min(100, tech_score))
    
    # Weighted Overall Score
    # SSL is most critical (40%), Headers (30%), DNS (20%), Tech (10%)
    overall_score = int(
        (ssl_score * 0.4) +
        (headers_score * 0.3) +
        (dns_score * 0.2) +
        (tech_score * 0.1)
    )
    
    # Risk Level
    if overall_score >= 90:
        risk_level = "Low"
    elif overall_score >= 70:
        risk_level = "Medium"
    elif overall_score >= 40:
        risk_level = "High"
    else:
        risk_level = "Critical"
        
    return {
        "overall_score": overall_score,
        "ssl_score": ssl_score,
        "headers_score": headers_score,
        "dns_score": dns_score,
        "tech_score": tech_score,
        "risk_level": risk_level
    }
