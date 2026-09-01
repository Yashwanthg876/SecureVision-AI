import os
import time
import json
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List

from app.ml.config.model_config import ISOLATION_FOREST_CONFIG
from app.ml.training.model_persistence import save_model

class IsolationForestTrainer:
    """
    Trains an Isolation Forest anomaly detection model to establish a global baseline 
    of website configurations.
    """
    def __init__(self, schema_version: str = "1.0"):
        self.model_name = "Isolation Forest"
        self.schema_version = schema_version
        self.config = ISOLATION_FOREST_CONFIG
        
        self.model = IsolationForest(**self.config)
        
    def train(self, X_train: np.ndarray, feature_names: List[str]) -> Dict[str, Any]:
        """
        Fits the Isolation Forest on the training dataset. Note: No y_train is needed
        because this is an unsupervised algorithm.
        """
        print("Training Isolation Forest Anomaly Engine...")
        start_time = time.time()
        
        self.model.fit(X_train)
        
        training_time = time.time() - start_time
        
        # Calculate training set anomaly scores to find distribution boundaries
        scores = self.model.decision_function(X_train)
        
        metadata = {
            "model_name": self.model_name,
            "model_version": self.schema_version,
            "feature_schema_version": self.schema_version,
            "hyperparameters": self.config,
            "training_time_s": training_time,
            "dataset_size": len(X_train),
            "score_distribution": {
                "mean": float(np.mean(scores)),
                "std": float(np.std(scores)),
                "min": float(np.min(scores)),
                "max": float(np.max(scores)),
                "percentile_5": float(np.percentile(scores, 5)),
                "percentile_10": float(np.percentile(scores, 10))
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        # Persist model
        save_model(self.model, self.model_name, self.schema_version)
        
        # Persist metadata
        meta_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'metadata'))
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "isolation_forest_metadata.json")
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=4)
            
        print(f"Isolation Forest trained in {training_time:.2f}s")
        return metadata
