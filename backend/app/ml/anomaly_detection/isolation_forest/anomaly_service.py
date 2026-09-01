import uuid
import numpy as np
from typing import List, Optional
from app.ml.anomaly_detection.isolation_forest.predictor import IsolationForestPredictor
from app.ml.anomaly_detection.isolation_forest.anomaly_reason_engine import AnomalyReasonEngine
from app.ml.anomaly_detection.isolation_forest.anomaly_history import AnomalyHistoryManager
from app.ml.anomaly_detection.isolation_forest.anomaly_schema import AnomalySchema, AnomalyTrendInfo

class AnomalyService:
    """
    Public interface for the Anomaly Detection Engine.
    """
    def __init__(self):
        # In a real setup, we'd load metadata to get global means/stds for the reason engine
        try:
            self.predictor = IsolationForestPredictor()
            self.reason_engine = AnomalyReasonEngine()
            self.history_manager = AnomalyHistoryManager()
            self.is_active = True
        except Exception as e:
            print(f"Anomaly Engine failed to initialize: {str(e)}")
            self.is_active = False
            
    def detect_anomaly(
        self, 
        feature_vector: np.ndarray, 
        feature_names: List[str],
        prediction_id: str = None,
        website_id: str = None
    ) -> Optional[AnomalySchema]:
        """
        Runs the anomaly detection pipeline and returns the complete AnomalySchema.
        """
        if not self.is_active:
            return None
            
        raw_score, prob, status, severity = self.predictor.predict_anomaly(feature_vector)
        
        top_features, category_scores = self.reason_engine.determine_contributions(
            feature_vector, feature_names
        )
        
        trend_info = None
        if website_id:
            history = self.history_manager.get_website_history(website_id)
            if history:
                scores = [h["score"] for h in history]
                hist_avg = sum(scores) / len(scores)
                deviation = raw_score - hist_avg
                
                # If the score is higher (closer to 1), it's less anomalous.
                is_improving = raw_score > scores[-1] if len(scores) > 0 else True
                
                trend_info = AnomalyTrendInfo(
                    is_improving=is_improving,
                    historical_average=hist_avg,
                    deviation_from_history=deviation
                )
                
        anomaly = AnomalySchema(
            anomaly_id=str(uuid.uuid4()),
            prediction_id=prediction_id,
            website_id=website_id,
            anomaly_score=raw_score,
            anomaly_probability=prob,
            status=status,
            severity=severity,
            category_scores=category_scores,
            top_contributing_features=top_features,
            trend_info=trend_info
        )
        
        # Log to history
        self.history_manager.log_anomaly(anomaly)
        
        return anomaly
