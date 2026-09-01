from typing import Dict, Any, Optional
from datetime import datetime

def extract_whois_features(whois_details: Dict[str, Any]) -> Optional[int]:
    """
    Extracts ML features from the WHOIS JSONB blob.
    Returns: domain_age_days
    """
    if not whois_details:
        return None
        
    creation_date_str = whois_details.get("creation_date")
    if not creation_date_str:
        return None
        
    try:
        # Assuming format like "2023-01-01T00:00:00"
        creation_date = datetime.fromisoformat(str(creation_date_str).replace('Z', '+00:00'))
        age = (datetime.now(creation_date.tzinfo) - creation_date).days
        return age if age > 0 else 0
    except (ValueError, TypeError):
        return None
