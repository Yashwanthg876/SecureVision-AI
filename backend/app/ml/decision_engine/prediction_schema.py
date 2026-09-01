from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class UnifiedPrediction(BaseModel):
    """
    The central prediction contract for the entire SecureVision AI platform.
    Future components (Dashboard, SHAP, Gemini) will consume this object.
    """
    prediction_id: str = Field(..., description="Unique UUID for this prediction run")
    prediction: str = Field(..., description="Final resolved risk classification (e.g. Critical, High, Medium, Low)")
    confidence: float = Field(..., description="Statistical confidence score between 0.0 and 1.0")
    confidence_level: str = Field(..., description="Human-readable confidence (Very High, High, Medium, Low, Very Low)")
    agreement_score: float = Field(..., description="Ratio of models agreeing with the final prediction")
    models_agreeing: int = Field(..., description="Number of models that predicted the final class")
    total_models: int = Field(..., description="Total number of models that participated in the decision")
    strategy: str = Field(..., description="The voting strategy used (e.g., Probability Averaging)")
    
    individual_predictions: Dict[str, str] = Field(..., description="Raw predictions from each model")
    probabilities: Dict[str, float] = Field(..., description="Final blended probability distribution across classes")
    model_versions: Dict[str, str] = Field(..., description="Versions of the models used in this decision")
    
    explanation: Optional[Dict[str, Any]] = Field(None, description="Reserved for Explainable AI (SHAP) integration")
    anomaly_result: Optional[Dict[str, Any]] = Field(None, description="Anomaly Detection Engine result schema")
