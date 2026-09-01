import os
import json
import csv
from typing import List, Dict, Any
from app.ml.anomaly_detection.isolation_forest.anomaly_schema import AnomalySchema

class AnomalyHistoryManager:
    """
    Manages the persistent storage of anomaly events.
    Prepares data for future LSTM trend prediction models.
    """
    def __init__(self):
        self.history_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'anomaly'))
        os.makedirs(self.history_dir, exist_ok=True)
        self.history_file = os.path.join(self.history_dir, "anomaly_history.csv")
        self._initialize_file()
        
    def _initialize_file(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "anomaly_id", "prediction_id", "website_id",
                    "score", "probability", "severity", "trend_is_improving",
                    "historical_average", "deviation"
                ])
                
    def log_anomaly(self, anomaly: AnomalySchema):
        """
        Logs the event. Normal events might be skipped or logged based on configuration,
        but for LSTM training, we want continuous history, so we log all assessments.
        """
        with open(self.history_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                anomaly.timestamp,
                anomaly.anomaly_id,
                anomaly.prediction_id or "",
                anomaly.website_id or "",
                anomaly.anomaly_score,
                anomaly.anomaly_probability,
                anomaly.severity,
                anomaly.trend_info.is_improving if anomaly.trend_info else "",
                anomaly.trend_info.historical_average if anomaly.trend_info else "",
                anomaly.trend_info.deviation_from_history if anomaly.trend_info else ""
            ])
            
    def get_website_history(self, website_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the time-series history for a specific website to calculate trends.
        """
        history = []
        if not os.path.exists(self.history_file):
            return history
            
        with open(self.history_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["website_id"] == website_id:
                    history.append({
                        "timestamp": row["timestamp"],
                        "score": float(row["score"])
                    })
        return sorted(history, key=lambda x: x["timestamp"])
