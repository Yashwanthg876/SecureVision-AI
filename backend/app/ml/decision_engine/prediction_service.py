import numpy as np
from typing import List, Dict, Any
from app.ml.decision_engine.decision_engine import DecisionEngine
from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from app.ml.config.decision_engine_config import DEFAULT_VOTING_STRATEGY

class PredictionService:
    """
    The unified prediction API boundary.
    No frontend or API should invoke individual models directly.
    """
    def __init__(self, class_labels: List[str] = None):
        if class_labels is None:
            # Default fallback if not provided; preferably passed dynamically via MLFeatureEncoder
            self.class_labels = ["Critical", "High", "Low", "Medium"]
        else:
            self.class_labels = class_labels
            
        self.decision_engine = DecisionEngine(self.class_labels)
        
        try:
            from app.ml.anomaly_detection.isolation_forest.anomaly_service import AnomalyService
            self.anomaly_service = AnomalyService()
        except ImportError:
            self.anomaly_service = None
        
    def predict_risk(self, feature_vector: np.ndarray, strategy: str = DEFAULT_VOTING_STRATEGY) -> UnifiedPrediction:
        """
        Takes an engineered numerical feature vector and returns the resolved unified prediction.
        """
        # Ensure 2D
        if feature_vector.ndim == 1:
            feature_vector = feature_vector.reshape(1, -1)
            
        prediction = self.decision_engine.predict(feature_vector, strategy=strategy)
        
        if self.anomaly_service:
            # We don't have feature_names easily accessible here unless passed, 
            # so we'll pass empty list or a generic one if not provided in the API signature yet.
            # In a real flow, feature_names comes from the ML pipeline.
            # For now, we'll pass an empty list and prediction id.
            anomaly = self.anomaly_service.detect_anomaly(
                feature_vector, 
                feature_names=[], # Will be injected by higher layer
                prediction_id=prediction.prediction_id
            )
            if anomaly:
                prediction.anomaly_result = anomaly.model_dump()
                
        return prediction
