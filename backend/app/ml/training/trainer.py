import time
import numpy as np
from typing import Any, Dict, Callable
from app.ml.training.experiment_logger import ExperimentLogger
from app.ml.training.model_persistence import save_model
from app.ml.evaluation.metrics import calculate_classification_metrics

class ModelTrainer:
    def __init__(self, model_name: str, model_factory: Callable, hyperparameters: Dict[str, Any], schema_version: str = "1.0"):
        self.model_name = model_name
        self.model = model_factory(**hyperparameters) if hyperparameters else model_factory()
        self.hyperparameters = hyperparameters
        self.schema_version = schema_version
        self.logger = ExperimentLogger()
        
    def save_metadata(self, 
                      dataset_size: int, 
                      val_size: int,
                      training_time: float, 
                      metrics: Dict[str, Any], 
                      cv_metrics: Dict[str, Any] = None,
                      feature_importance_path: str = None):
        import os
        import json
        import sklearn
        from datetime import datetime
        
        metadata = {
            "model_name": self.model_name,
            "model_version": self.schema_version, # Defaulting to schema_version as model version for now
            "feature_schema_version": self.schema_version,
            "dataset_version": "1.0",
            "training_timestamp": datetime.utcnow().isoformat(),
            "training_dataset_size": dataset_size,
            "validation_dataset_size": val_size,
            "test_dataset_size": val_size,
            "hyperparameters": self.hyperparameters,
            "accuracy": metrics.get("accuracy"),
            "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "f1_score": metrics.get("f1_score"),
            "roc_auc": metrics.get("roc_auc"),
            "training_duration": training_time,
            "scikit_learn_version": sklearn.__version__
        }
        
        if cv_metrics:
            metadata["cross_validation"] = cv_metrics
            
        if feature_importance_path:
            metadata["feature_importance_file"] = feature_importance_path
            
        metadata_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'metadata')
        os.makedirs(metadata_dir, exist_ok=True)
        
        safe_name = self.model_name.replace(" ", "_").lower()
        metadata_path = os.path.join(metadata_dir, f"{safe_name}_metadata.json")
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
            
    def train_and_evaluate(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, cv_metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Trains the model, evaluates it on the validation set, and logs the experiment.
        """
        start_time = time.time()
        
        # Train
        self.model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        
        # Evaluate
        y_pred = self.model.predict(X_val)
        y_prob = self.model.predict_proba(X_val) if hasattr(self.model, "predict_proba") else None
        
        metrics = calculate_classification_metrics(y_val, y_pred, y_prob)
        
        # Log
        self.logger.log_experiment(
            model_name=self.model_name,
            schema_version=self.schema_version,
            hyperparameters=self.hyperparameters,
            dataset_size=len(X_train) + len(X_val),
            training_time_s=training_time,
            metrics=metrics
        )
        
        # Metadata
        self.save_metadata(
            dataset_size=len(X_train),
            val_size=len(X_val),
            training_time=training_time,
            metrics=metrics,
            cv_metrics=cv_metrics
        )
        
        # Persist
        save_model(self.model, self.model_name, self.schema_version)
        
        return metrics
