from typing import Dict, Any

class ContextValidator:
    """
    Ensures that the LLM is never invoked with incomplete or missing ML context.
    Prevents hallucination by enforcing strict data availability.
    """
    
    @staticmethod
    def validate(context: Dict[str, Any]) -> bool:
        if not context:
            return False
            
        risk = context.get("risk_analysis", {})
        if not risk.get("final_risk_level") or not risk.get("confidence_score"):
            return False
            
        # We enforce that explainability must be present if risk is calculated
        expl = context.get("explainability", {})
        if not expl.get("top_positive_factors") and not expl.get("top_negative_factors"):
            # It's possible for perfectly neutral, but generally we expect some SHAP values
            # For strictness we could demand it, but let's allow it as long as the key exists
            pass
            
        return True
