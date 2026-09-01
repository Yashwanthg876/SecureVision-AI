import numpy as np
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

class FeatureDriftMonitor:
    """
    Lightweight feature drift monitoring module.
    Compares prediction-time feature distributions with the original training dataset.
    """
    def __init__(self, training_data_stats: Dict[str, Dict[str, float]], threshold_percent: float = 15.0):
        """
        :param training_data_stats: A dictionary where keys are feature names and values are 
                                    dictionaries containing 'mean' and 'std' from training time.
        :param threshold_percent: The percentage difference threshold to trigger a drift warning.
        """
        self.training_stats = training_data_stats
        self.threshold_percent = threshold_percent
        
    def detect_drift(self, incoming_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Computes statistical summaries for the incoming batch and detects deviations.
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "drift_detected": False,
            "drifted_features": [],
            "warnings": []
        }
        
        for feature in incoming_data.columns:
            if feature not in self.training_stats:
                continue
                
            # Compute incoming stats (assuming numerical features)
            if not pd.api.types.is_numeric_dtype(incoming_data[feature]):
                continue
                
            incoming_mean = incoming_data[feature].mean()
            training_mean = self.training_stats[feature].get("mean", 0)
            
            if training_mean == 0:
                if incoming_mean == 0:
                    diff_pct = 0
                else:
                    diff_pct = 100.0 # Arbitrary high difference if baseline was 0 and now isn't
            else:
                diff_pct = abs(incoming_mean - training_mean) / abs(training_mean) * 100.0
                
            if diff_pct > self.threshold_percent:
                severity = "High" if diff_pct > (self.threshold_percent * 2) else "Medium"
                report["drift_detected"] = True
                report["drifted_features"].append(feature)
                report["warnings"].append({
                    "feature": feature,
                    "training_mean": float(training_mean),
                    "incoming_mean": float(incoming_mean),
                    "percentage_difference": float(diff_pct),
                    "drift_severity": severity
                })
                
        return report
