from typing import Dict, Any, Tuple, Optional

def extract_ssl_features(ssl_details: Dict[str, Any]) -> Tuple[Optional[bool], Optional[int], Optional[str]]:
    """
    Extracts ML features from the SSL JSONB blob.
    Returns: (is_valid, cert_expiry_days, tls_version)
    """
    if not ssl_details:
        return None, None, None
        
    is_valid = ssl_details.get("is_valid", False)
    cert_expiry_days = ssl_details.get("expires_in_days", 0)
    tls_version = ssl_details.get("tls_version", "Unknown")
    
    return is_valid, cert_expiry_days, tls_version
