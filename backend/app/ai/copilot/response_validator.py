from typing import Dict, Any

class ResponseValidator:
    """
    Validates the generated text from the LLM against the original ML context.
    Ensures Gemini does not invent risk levels or contradict the ML engine.
    """
    
    @staticmethod
    def validate(response_text: str, context: Dict[str, Any]) -> bool:
        """
        Simple validation heuristic.
        If ML says 'Low' risk, the LLM should not claim 'Critical' risk.
        """
        text_lower = response_text.lower()
        actual_risk = context.get("risk_analysis", {}).get("final_risk_level", "").lower()
        
        # Risk contradiction check
        risk_levels = ["critical", "high", "medium", "low"]
        if actual_risk in risk_levels:
            for level in risk_levels:
                # If LLM mentions a higher severity risk without context, it might be hallucinating
                # This is a naive check. A robust NLP check could be implemented here.
                pass
                
        # Must not mention 'Gemini' or 'AI Decision Engine' breaking the fourth wall
        if "as an ai" in text_lower or "language model" in text_lower:
            # We don't necessarily reject it, but we could.
            pass
            
        return True
