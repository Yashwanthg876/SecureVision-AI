import numpy as np
from typing import Tuple, Dict, Any
from app.ml.training.model_persistence import load_model

class IsolationForestPredictor:
    """
    Handles inference for the Isolation Forest anomaly detection model.
    """
    def __init__(self, model_version: str = "1.0", metadata: Dict[str, Any] = None):
        self.model = load_model("Isolation Forest", model_version)
        self.metadata = metadata or {}
        
    def predict_anomaly(self, feature_vector: np.ndarray) -> Tuple[float, float, str, str]:
        """
        Returns:
        - raw_score: Negative means more anomalous
        - probability: 0 to 1 normalized anomaly probability
        - status: "Normal" or "Anomalous"
        - severity: "Normal", "Suspicious", "Anomalous", "Critical Anomaly"
        """
        raw_score = float(self.model.decision_function(feature_vector)[0])
        label = int(self.model.predict(feature_vector)[0]) # 1 = normal, -1 = anomalous
        
        # Normalize score to a 0-1 probability-like metric
        # Isolation Forest decision_function generally ranges near -0.5 to 0.5. 
        # Scikit-learn normalizes somewhat but we can bound it.
        # Negative scores are anomalies. So max anomaly = -1. Max normal = 1 (theoretically).
        # We map [-0.5, 0.5] -> [1, 0] approx, so higher probability = more anomalous.
        normalized_prob = max(0.0, min(1.0, 0.5 - raw_score))
        
        status = "Anomalous" if label == -1 else "Normal"
        
        # Determine Severity using metadata boundaries if available, else static thresholds
        stats = self.metadata.get("score_distribution", {})
        mean_score = stats.get("mean", 0.0)
        p10 = stats.get("percentile_10", -0.1)
        p5 = stats.get("percentile_5", -0.2)
        
        if raw_score >= p10:
            severity = "Normal"
            status = "Normal" # override just in case label was -1 but very borderline
        elif p5 <= raw_score < p10:
            severity = "Suspicious"
            status = "Anomalous"
        elif raw_score < p5 and raw_score > (p5 - 0.15):
            severity = "Anomalous"
            status = "Anomalous"
        else:
            severity = "Critical Anomaly"
            status = "Anomalous"
            
        return raw_score, normalized_prob, status, severity
