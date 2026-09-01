import os
import json
import csv
from datetime import datetime
from typing import Dict, Any

class ExperimentLogger:
    def __init__(self, log_dir: str = "backend/app/ml/logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.csv_path = os.path.join(self.log_dir, "experiments.csv")
        self._init_csv()

    def _init_csv(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "model_name", "feature_schema_version", 
                    "dataset_size", "training_time_s", "accuracy", "f1_score", "roc_auc",
                    "feature_importance_path"
                ])

    def log_experiment(self, 
                       model_name: str, 
                       schema_version: str, 
                       hyperparameters: Dict[str, Any], 
                       dataset_size: int, 
                       training_time_s: float, 
                       metrics: Dict[str, Any],
                       feature_importance_path: str = None):
        """
        Logs experiment to both CSV and a detailed JSON file.
        """
        timestamp = datetime.utcnow().isoformat()
        
        # Append to CSV summary
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                model_name,
                schema_version,
                dataset_size,
                round(training_time_s, 2),
                metrics.get("accuracy", ""),
                metrics.get("f1_score", ""),
                metrics.get("roc_auc", ""),
                feature_importance_path or ""
            ])
            
        # Write detailed JSON log
        log_entry = {
            "timestamp": timestamp,
            "model_name": model_name,
            "feature_schema_version": schema_version,
            "hyperparameters": hyperparameters,
            "dataset_size": dataset_size,
            "training_time_s": training_time_s,
            "metrics": metrics,
            "feature_importance_path": feature_importance_path
        }
        
        safe_name = model_name.replace(" ", "_").lower()
        json_filename = f"exp_{safe_name}_{datetime.utcnow().strftime('%Y%md_%H%M%S')}.json"
        json_path = os.path.join(self.log_dir, json_filename)
        
        with open(json_path, 'w') as f:
            json.dump(log_entry, f, indent=4)
