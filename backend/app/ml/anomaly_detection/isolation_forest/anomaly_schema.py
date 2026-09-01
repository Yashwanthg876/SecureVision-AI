from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class AnomalyTrendInfo(BaseModel):
    is_improving: bool = Field(..., description="True if anomaly score is getting closer to 0 compared to last assessment")
    historical_average: float = Field(..., description="The running average of anomaly scores for this website")
    deviation_from_history: float = Field(..., description="How far this score deviates from the website's own historical average")

class AnomalySchema(BaseModel):
    anomaly_id: str = Field(..., description="Unique UUID for this anomaly event")
    prediction_id: Optional[str] = Field(None, description="UUID of the corresponding risk prediction")
    website_id: Optional[str] = Field(None, description="UUID of the website being assessed")
    
    anomaly_score: float = Field(..., description="Raw Isolation Forest decision_function score (-1 to 1). Lower is more anomalous.")
    anomaly_probability: float = Field(..., description="Normalized score (0 to 1). 1 is highly anomalous.")
    
    status: str = Field(..., description="Binary 'Normal' or 'Anomalous'")
    severity: str = Field(..., description="Severity mapping: 'Normal', 'Suspicious', 'Anomalous', 'Critical Anomaly'")
    
    category_scores: Dict[str, float] = Field(default_factory=dict, description="Anomaly impact broken down by feature category")
    top_contributing_features: List[str] = Field(default_factory=list, description="Top features driving the anomaly")
    
    trend_info: Optional[AnomalyTrendInfo] = Field(None, description="Historical trend comparison for the same website")
    
    recommended_action: Optional[str] = Field(None, description="Reserved for future Gemini AI integration")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO timestamp")
