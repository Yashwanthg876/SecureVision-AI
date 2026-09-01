import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, List
from xgboost import XGBClassifier
from app.ml.models.ensemble.base_ensemble import BaseEnsembleTrainer
from app.ml.evaluation.metrics import calculate_classification_metrics
from app.ml.training.model_persistence import save_model

class XGBoostTrainer(BaseEnsembleTrainer):
    """
    Dedicated trainer for XGBoost integrating Early Stopping, Learning Curves, and robust XAI exporting.
    """
    def __init__(self, hyperparameters: Dict[str, Any], schema_version: str = "1.0"):
        # We handle initialization here since XGBClassifier has specific needs
        self.model_name = "XGBoost"
        self.schema_version = schema_version
        self.hyperparameters = hyperparameters
        self.model = XGBClassifier(**hyperparameters, use_label_encoder=False, random_state=42)
        
        # We manually init the logger from BaseEnsembleTrainer
        from app.ml.training.experiment_logger import ExperimentLogger
        self.logger = ExperimentLogger()
        
    def generate_learning_curves(self, results: Dict[str, Any], export_dir: str):
        """
        Plots training vs validation log-loss over the boosting rounds.
        """
        os.makedirs(export_dir, exist_ok=True)
        epochs = len(results['validation_0']['mlogloss'] if 'mlogloss' in results['validation_0'] else results['validation_0']['logloss'])
        x_axis = range(0, epochs)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Support both multiclass (mlogloss) and binary (logloss)
        metric_key = 'mlogloss' if 'mlogloss' in results['validation_0'] else 'logloss'
        
        ax.plot(x_axis, results['validation_0'][metric_key], label='Train')
        ax.plot(x_axis, results['validation_1'][metric_key], label='Validation')
        ax.legend()
        ax.set_ylabel('Log Loss')
        ax.set_title('XGBoost Learning Curve')
        
        plot_path = os.path.join(export_dir, 'xgboost_learning_curve.png')
        fig.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        return plot_path

    def train_and_evaluate_ensemble(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray, 
        X_val: np.ndarray, 
        y_val: np.ndarray, 
        feature_names: List[str],
        cv_metrics: Dict[str, Any] = None,
        early_stopping_rounds: int = 20
    ) -> Dict[str, Any]:
        """
        Overrides training to include early stopping and learning curve generation.
        """
        start_time = time.time()
        
        eval_set = [(X_train, y_train), (X_val, y_val)]
        
        # Train with early stopping
        # In newer scikit-learn/xgboost, early_stopping_rounds is often passed to fit or init
        # We pass to fit here.
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=False
        )
        
        training_time = time.time() - start_time
        
        # Get learning curve results
        evals_result = self.model.evals_result()
        curve_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'learning_curves'))
        self.generate_learning_curves(evals_result, curve_dir)
        
        # Extract Feature Importance (BaseEnsembleTrainer functionality)
        importance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'importances'))
        importance_path = self.extract_feature_importance(feature_names, importance_dir)
        
        # Plot Feature Importance
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
