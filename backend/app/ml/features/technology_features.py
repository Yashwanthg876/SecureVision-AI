from typing import Dict, Any, Tuple, Optional

def extract_technology_features(tech_details: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts ML features from the Technology JSONB blob.
    Returns: (server_software, framework)
    """
    if not tech_details:
        return None, None
        
    server = tech_details.get("server", None)
    framework = tech_details.get("x_powered_by", None)
    
    return server, framework
