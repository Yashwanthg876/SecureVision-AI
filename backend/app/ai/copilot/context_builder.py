from typing import Dict, Any, Optional
from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from app.ml.trend_prediction.trend_schema import TrendSchema

class ContextBuilder:
    """
    Bridges ML and AI. Gathers raw ML outputs and crushes them into 
    a highly structured JSON context object that is safe for LLM consumption.
    """
    
    @staticmethod
    def build_context(
        prediction: UnifiedPrediction, 
        trend: Optional[TrendSchema] = None
    ) -> Dict[str, Any]:
        
        context = {
            "assessment_metadata": {
                "prediction_id": prediction.prediction_id,
            },
            "risk_analysis": {
                "final_risk_level": prediction.prediction,
                "confidence_score": prediction.confidence,
                "confidence_level": prediction.confidence_level
            },
            "explainability": {},
            "anomaly_detection": {},
            "trend_forecast": {}
        }
        
        if prediction.explanation:
            context["explainability"] = {
                "top_positive_factors": [f["feature"] for f in prediction.explanation.get("top_positive_features", [])],
                "top_negative_factors": [f["feature"] for f in prediction.explanation.get("top_negative_features", [])],
                "summary": prediction.explanation.get("summary", "")
            }
            
        if prediction.anomaly_result:
            context["anomaly_detection"] = {
                "status": prediction.anomaly_result.get("status"),
                "severity": prediction.anomaly_result.get("severity"),
                "anomaly_score": prediction.anomaly_result.get("anomaly_score"),
                "top_contributing_features": prediction.anomaly_result.get("top_contributing_features", [])
            }
            
        if trend:
            context["trend_forecast"] = {
                "direction": trend.overall_trend_direction,
                "confidence": trend.confidence,
                "next_30_days_score": trend.forecasts[-1].predicted_security_score if trend.forecasts else None
            }
            
        return context
