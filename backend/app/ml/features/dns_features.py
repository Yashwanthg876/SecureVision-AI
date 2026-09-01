from typing import Dict, Any, Tuple

def extract_dns_features(dns_details: Dict[str, Any]) -> Tuple[bool, bool]:
    """
    Extracts ML features from the DNS JSONB blob.
    Returns: (has_spf, has_dmarc)
    """
    if not dns_details:
        return False, False
        
    has_spf = dns_details.get("has_spf", False)
    has_dmarc = dns_details.get("has_dmarc", False)
    
    return has_spf, has_dmarc
