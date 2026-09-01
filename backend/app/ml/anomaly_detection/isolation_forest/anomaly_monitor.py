import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any

class AnomalyMonitor:
    """
    Monitors anomaly trends across the entire platform.
    Prepares payloads for dashboards and reporting.
    """
    def __init__(self):
        self.history_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'anomaly'))
        self.history_file = os.path.join(self.history_dir, "anomaly_history.csv")
        
    def generate_dashboard_payload(self) -> Dict[str, Any]:
        """
        Generates aggregated metrics for Risk vs. Anomaly Matrices and Heatmaps.
        """
        payload = {
            "daily_anomaly_count": 0,
            "weekly_anomaly_trends": [],
            "average_anomaly_score": 0.0,
            "severity_distribution": {
                "Normal": 0,
                "Suspicious": 0,
                "Anomalous": 0,
                "Critical Anomaly": 0
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if not os.path.exists(self.history_file):
            return payload
            
        import csv
        today = datetime.utcnow().date()
        scores = []
        
        with open(self.history_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.fromisoformat(row["timestamp"]).date()
                if dt == today:
                    if row["status"] == "Anomalous":
                        payload["daily_anomaly_count"] += 1
                        
                severity = row.get("severity", "Normal")
                if severity in payload["severity_distribution"]:
                    payload["severity_distribution"][severity] += 1
                    
                scores.append(float(row["score"]))
                
        if scores:
            payload["average_anomaly_score"] = sum(scores) / len(scores)
            
        return payload
