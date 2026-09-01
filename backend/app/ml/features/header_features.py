from typing import Dict, Any, Tuple

def extract_header_features(header_details: Dict[str, Any]) -> Tuple[bool, bool, bool, bool]:
    """
    Extracts ML features from the HTTP Headers JSONB blob.
    Returns: (has_hsts, has_csp, has_x_frame_options, has_x_content_type_options)
    """
    if not header_details:
        return False, False, False, False
        
    has_hsts = header_details.get("strict_transport_security", False)
    has_csp = header_details.get("content_security_policy", False)
    has_x_frame_options = header_details.get("x_frame_options", False)
    has_x_content_type_options = header_details.get("x_content_type_options", False)
    
    return has_hsts, has_csp, has_x_frame_options, has_x_content_type_options
