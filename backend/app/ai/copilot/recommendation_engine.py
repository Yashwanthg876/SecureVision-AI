from typing import List, Dict, Any

class RecommendationEngine:
    """
    Translates raw ML vulnerability findings into a prioritized list of actionable recommendations.
    """
    
    def __init__(self):
        # A mock knowledge base mapping features to recommendations and severities
        self.kb = {
            "strict_transport_security": {"action": "Enable HSTS (Strict-Transport-Security) header.", "severity": "High"},
            "content_security_policy": {"action": "Implement a Content-Security-Policy (CSP) to mitigate XSS.", "severity": "Critical"},
            "x_frame_options": {"action": "Configure X-Frame-Options to prevent Clickjacking.", "severity": "Medium"},
            "ssl_expired": {"action": "Renew expired SSL certificate immediately.", "severity": "Critical"}
        }

    def generate_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        recs = []
        
        # Look at top negative factors from SHAP
        negative_factors = context.get("explainability", {}).get("top_negative_factors", [])
        for factor in negative_factors:
            if factor in self.kb:
                recs.append({
                    "action": self.kb[factor]["action"],
                    "severity": self.kb[factor]["severity"],
                    "source": "SHAP Explainability"
                })
                
        # Look at anomaly contributing features
        anomaly_features = context.get("anomaly_detection", {}).get("top_contributing_features", [])
        for feature in anomaly_features:
            if feature not in negative_factors: # Avoid duplicates
                recs.append({
                    "action": f"Investigate anomalous behavior in {feature}",
                    "severity": "Medium",
                    "source": "Isolation Forest Anomaly Engine"
                })
                
        # Sort by severity (Critical > High > Medium > Low)
        severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        recs.sort(key=lambda x: severity_order.get(x["severity"], 5))
        
        return recs
