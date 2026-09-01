import numpy as np
import pandas as pd
from typing import Callable, Dict, Any, List, Union
from sklearn.model_selection import StratifiedKFold
from app.ml.evaluation.metrics import calculate_classification_metrics

def evaluate_with_kfold(
    data: Union[pd.DataFrame, np.ndarray], 
    y_or_factory: Union[np.ndarray, Callable] = None, 
    model_factory: Callable = None, 
    n_splits: int = 5, 
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Performs 5-Fold Stratified Cross Validation.
    If 'data' is a pandas DataFrame, MLFeatureEncoder is fitted strictly inside 
    each training fold (zero preprocessing leakage).
    """
    from app.ml.encoders.feature_encoder import MLFeatureEncoder
    
    if isinstance(data, pd.DataFrame):
        df = data.copy()
        factory = y_or_factory if callable(y_or_factory) else model_factory
        y_labels = df['label'].values
        
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        cv_metrics = {"accuracy": [], "precision": [], "recall": [], "f1_score": [], "roc_auc": []}
        
        for train_idx, val_idx in skf.split(df, y_labels):
            df_train_fold = df.iloc[train_idx].copy()
            df_val_fold = df.iloc[val_idx].copy()
            
            # FIT ENCODER ONLY ON TRAINING FOLD
            encoder = MLFeatureEncoder()
            X_train_fold, y_train_fold = encoder.fit_transform(df_train_fold, save_artifacts=False)
            
            # TRANSFORM VALIDATION FOLD USING ONLY FITTED TRAINING ENCODER
            X_val_fold = encoder.transform(df_val_fold)
            y_val_fold = encoder.label_encoder.transform(df_val_fold['label'])
            
            model = factory()
            model.fit(X_train_fold, y_train_fold)
            
            y_pred = model.predict(X_val_fold)
            y_prob = model.predict_proba(X_val_fold) if hasattr(model, "predict_proba") else None
            
            metrics = calculate_classification_metrics(y_val_fold, y_pred, y_prob)
            for k, v in metrics.items():
                if v is not None:
                    cv_metrics[k].append(v)
    else:
        # Fallback for pre-split numpy arrays
        X = data
        y = y_or_factory
        factory = model_factory
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        cv_metrics = {"accuracy": [], "precision": [], "recall": [], "f1_score": [], "roc_auc": []}
        
        for train_idx, val_idx in skf.split(X, y):
            X_train_fold, X_val_fold = X[train_idx], X[val_idx]
            y_train_fold, y_val_fold = y[train_idx], y[val_idx]
            
            model = factory()
            model.fit(X_train_fold, y_train_fold)
            
            y_pred = model.predict(X_val_fold)
            y_prob = model.predict_proba(X_val_fold) if hasattr(model, "predict_proba") else None
            
            metrics = calculate_classification_metrics(y_val_fold, y_pred, y_prob)
            for k, v in metrics.items():
                if v is not None:
                    cv_metrics[k].append(v)
                    
    summary = {}
    for k, v in cv_metrics.items():
        if v:
            summary[f"{k}_folds"] = v
            summary[f"mean_{k}"] = float(np.mean(v))
            summary[f"std_{k}"] = float(np.std(v))
            summary[f"min_{k}"] = float(np.min(v))
            summary[f"max_{k}"] = float(np.max(v))
            
    return summary
