from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FeatureContribution(BaseModel):
    feature: str = Field(..., description="Human-readable feature name")
    impact: float = Field(..., description="SHAP value indicating directional impact")

class ExplanationSchema(BaseModel):
    explanation_id: str = Field(..., description="Unique UUID for this explanation")
    prediction_id: str = Field(..., description="UUID of the corresponding prediction")
    prediction: str = Field(..., description="Final resolved risk classification")
    confidence: float = Field(..., description="Confidence score mapped from prediction")
    explanation_confidence: str = Field(..., description="Confidence level of the explanation stability")
    
    top_positive_features: List[FeatureContribution] = Field(default_factory=list, description="Features pushing risk higher")
    top_negative_features: List[FeatureContribution] = Field(default_factory=list, description="Features pushing risk lower")
    
    category_contributions: Dict[str, float] = Field(default_factory=dict, description="Aggregated SHAP impacts by category (e.g., SSL, Headers, DNS)")
    
    summary: str = Field(..., description="Rule-based human readable summary of the explanation")
    recommendations: Optional[List[str]] = Field(default_factory=list, description="Reserved for future Gemini AI integration")
    
    model_versions: Dict[str, str] = Field(default_factory=dict, description="Versions of the models used in this decision")
    timestamp: str = Field(..., description="ISO timestamp of explanation generation")
