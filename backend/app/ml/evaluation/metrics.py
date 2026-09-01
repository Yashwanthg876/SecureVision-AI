import numpy as np
from typing import Dict, Any
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    classification_report
)

def calculate_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> Dict[str, Any]:
    """
    Calculates standard classification metrics.
    Works for both binary and multiclass by defaulting to 'weighted' average.
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1_score": f1_score(y_true, y_pred, average="weighted", zero_division=0)
    }
    
    if y_prob is not None:
        try:
            # Handle multiclass ROC AUC
            if len(y_prob.shape) > 1 and y_prob.shape[1] > 2:
                metrics["roc_auc"] = roc_auc_score(y_true, y_prob, multi_class="ovr", average="weighted")
            else:
                # Binary ROC AUC expects 1D array of probabilities for the positive class
                if len(y_prob.shape) == 2:
                    y_prob = y_prob[:, 1]
                metrics["roc_auc"] = roc_auc_score(y_true, y_prob)
        except Exception as e:
            metrics["roc_auc"] = None
            print(f"Warning: ROC-AUC calculation failed: {e}")
            
    return metrics

def generate_classification_report(y_true: np.ndarray, y_pred: np.ndarray, target_names: list = None) -> str:
    """
    Generates a formatted text report showing the main classification metrics.
    """
    return classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
