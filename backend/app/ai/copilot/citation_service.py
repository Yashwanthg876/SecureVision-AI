from typing import Dict, Any, List

class CitationService:
    """
    Traces AI-generated recommendations and facts back to their originating ML component
    (e.g., XGBoost, Isolation Forest, LSTM) to improve transparency and auditability.
    """
    
    @staticmethod
    def append_citations(recommendations: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Takes a list of recommendations and ensures they have a documented source.
        """
        for rec in recommendations:
            if "source" not in rec or not rec["source"]:
                rec["source"] = "AI Decision Engine (General)"
        return recommendations
        
    @staticmethod
    def build_citation_footer(context: Dict[str, Any]) -> str:
        """
        Builds a footer string detailing which ML models contributed to the context.
        """
        sources = []
        if context.get("risk_analysis"):
            sources.append("XGBoost (Risk Classification)")
        if context.get("explainability"):
            sources.append("SHAP (Feature Importance)")
        if context.get("anomaly_detection"):
            sources.append("Isolation Forest (Anomaly Engine)")
        if context.get("trend_forecast"):
            sources.append("LSTM (Trend Forecaster)")
            
        if sources:
            return "\n\n---\n**Citations:** This report was generated using data from: " + ", ".join(sources)
        return ""
