from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ConfidenceInterval(BaseModel):
    lower_bound: float = Field(..., description="Lower limit of the predicted value")
    upper_bound: float = Field(..., description="Upper limit of the predicted value")

class Forecast(BaseModel):
    horizon: str = Field(..., description="E.g., 'Next Assessment', '7 Days', '30 Days'")
    predicted_security_score: float = Field(..., description="The predicted future security score")
    predicted_risk_level: str = Field(..., description="The mapped future risk level (Critical, High, Medium, Low)")
    predicted_anomaly_probability: float = Field(..., description="Likelihood of the next assessment being anomalous")
    security_score_ci: ConfidenceInterval = Field(..., description="Uncertainty bounds for the score")
    forecast_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class TrendSchema(BaseModel):
    trend_id: str = Field(..., description="Unique UUID for this trend forecast")
    website_id: str = Field(..., description="Website being forecasted")
    
    overall_trend_direction: str = Field(..., description="Rapid Improvement, Improving, Stable, Slight Decline, Rapid Decline, Critical Decline")
    confidence: float = Field(..., description="Statistical confidence in the trend direction (0-100)")
    
    forecasts: List[Forecast] = Field(..., description="Predictions across multiple time horizons")
    
    trend_drivers: List[str] = Field(default_factory=list, description="Reserved for Gemini: Features driving the trend")
    recommended_action: Optional[str] = Field(None, description="Reserved for Gemini: Strategic recommendation")
    
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
