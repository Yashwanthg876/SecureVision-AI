import numpy as np
from typing import Any, Dict
from app.ml.evaluation.metrics import calculate_classification_metrics, generate_classification_report
from app.ml.evaluation.confusion_matrix import plot_confusion_matrix
from app.ml.evaluation.roc_curve import plot_roc_curve
from app.ml.evaluation.precision_recall import plot_precision_recall_curve

class ModelEvaluator:
    def __init__(self, model: Any, class_names: list):
        self.model = model
        self.class_names = class_names
        
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """
        Generates full test suite evaluation including metrics and text reports.
        """
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test) if hasattr(self.model, "predict_proba") else None
        
        metrics = calculate_classification_metrics(y_test, y_pred, y_prob)
        report = generate_classification_report(y_test, y_pred, target_names=self.class_names)
        
        metrics["classification_report"] = report
        
        return metrics
        
    def generate_visualizations(self, X_test: np.ndarray, y_test: np.ndarray, save_dir: str):
        """
        Generates and saves visual evaluation plots.
        """
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test) if hasattr(self.model, "predict_proba") else None
        
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        plot_confusion_matrix(y_test, y_pred, self.class_names, save_path=os.path.join(save_dir, "confusion_matrix.png"))
        
        if y_prob is not None:
            n_classes = len(self.class_names)
            plot_roc_curve(y_test, y_prob, n_classes, save_path=os.path.join(save_dir, "roc_curve.png"))
            plot_precision_recall_curve(y_test, y_prob, n_classes, save_path=os.path.join(save_dir, "precision_recall_curve.png"))
