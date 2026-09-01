import os
import json
import numpy as np
import pandas as pd
from typing import Any, Dict, List
from app.ml.training.trainer import ModelTrainer
from app.ml.training.experiment_logger import ExperimentLogger
from app.ml.training.model_persistence import save_model
from app.ml.evaluation.metrics import calculate_classification_metrics

class BaseEnsembleTrainer(ModelTrainer):
    """
    Extends the standard ModelTrainer with specific functionality for 
    ensemble models (like Random Forest, Extra Trees, XGBoost), primarily 
    focused on extracting and exporting feature importances.
    """
    
    def extract_feature_importance(self, feature_names: List[str], save_dir: str) -> str:
        """
        Extracts feature importances from the trained ensemble model,
        ranks them, and saves them to a JSON file.
        Returns the path to the saved JSON file.
        """
        if not hasattr(self.model, "feature_importances_"):
            print(f"Warning: Model {self.model_name} does not expose feature_importances_")
            return ""
            
        importances = self.model.feature_importances_
        
        # Ensure we don't crash if feature_names length mismatches (e.g. if one-hot encoding expanded features but we didn't get them all)
        if len(feature_names) != len(importances):
            print(f"Warning: Feature names count ({len(feature_names)}) does not match importances count ({len(importances)})")
            # Create generic names if mismatch
            feature_names = [f"Feature_{i}" for i in range(len(importances))]
            
        # Pair up and sort
        importance_dict = {name: float(imp) for name, imp in zip(feature_names, importances)}
        sorted_importance = dict(sorted(importance_dict.items(), key=lambda item: item[1], reverse=True))
        
        os.makedirs(save_dir, exist_ok=True)
        safe_name = self.model_name.replace(" ", "_").lower()
        file_path = os.path.join(save_dir, f"{safe_name}_feature_importance_{self.schema_version}.json")
        
        with open(file_path, 'w') as f:
            json.dump(sorted_importance, f, indent=4)
            
        return file_path

    def train_and_evaluate_ensemble(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray, 
        X_val: np.ndarray, 
        y_val: np.ndarray, 
        feature_names: List[str],
        cv_metrics: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Overrides training to include feature importance extraction.
        """
        import time
        start_time = time.time()
        
        # Train
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Extract Feature Importance
        importance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'importances'))
        importance_path = self.extract_feature_importance(feature_names, importance_dir)
        
        # Plot Feature Importance
        import matplotlib.pyplot as plt # type: ignore
        from matplotlib.figure import Figure # type: ignore
        
        with open(importance_path, 'r') as f:
            sorted_importance = json.load(f)
            
        top_20 = dict(list(sorted_importance.items())[:20])
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(list(top_20.keys())[::-1], list(top_20.values())[::-1], color='skyblue')
        ax.set_xlabel('Importance Score')
        ax.set_title(f'Top 20 Feature Importances - {self.model_name}')
        
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'feature_importance'))
        os.makedirs(reports_dir, exist_ok=True)
        safe_name = self.model_name.replace(" ", "_").lower()
        plot_path = os.path.join(reports_dir, f"{safe_name}_feature_importance_{self.schema_version}.png")
        fig.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        
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
            metrics=metrics,
            feature_importance_path=importance_path
        )
        
        # Metadata
        self.save_metadata(
            dataset_size=len(X_train),
            val_size=len(X_val),
            training_time=training_time,
            metrics=metrics,
            cv_metrics=cv_metrics,
            feature_importance_path=importance_path
        )
        
        # Persist
        save_model(self.model, self.model_name, self.schema_version)
        
        return metrics
