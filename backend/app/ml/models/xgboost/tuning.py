import pandas as pd
import numpy as np
import os
from typing import Dict, Any, Tuple
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

class XGBoostTuner:
    """
    Performs RandomizedSearchCV for XGBoost hyperparameters.
    """
    def __init__(self):
        self.param_distributions = {
            'n_estimators': [50, 100, 200, 300],
            'max_depth': [3, 5, 7, 10],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0],
            'gamma': [0, 0.1, 0.5, 1],
            'min_child_weight': [1, 3, 5],
            'reg_alpha': [0, 0.1, 1],
            'reg_lambda': [1, 1.5, 2]
        }
        
    def tune(self, X_train: np.ndarray, y_train: np.ndarray, n_iter: int = 20) -> Tuple[Dict[str, Any], pd.DataFrame]:
        """
        Tunes hyperparameters and returns the best params and the search history dataframe.
        """
        # Determine number of classes
        num_classes = len(np.unique(y_train))
        objective = 'multi:softprob' if num_classes > 2 else 'binary:logistic'
        
        base_estimator = XGBClassifier(
            objective=objective,
            eval_metric='mlogloss' if num_classes > 2 else 'logloss',
            use_label_encoder=False,
            random_state=42
        )
        
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        
        search = RandomizedSearchCV(
            estimator=base_estimator,
            param_distributions=self.param_distributions,
            n_iter=n_iter,
            scoring='roc_auc' if num_classes == 2 else 'roc_auc_ovr',
            cv=cv,
            n_jobs=-1,
            random_state=42,
            verbose=1
        )
        
        search.fit(X_train, y_train)
        
        cv_results_df = pd.DataFrame(search.cv_results_)
        
        return search.best_params_, cv_results_df

    def export_history(self, cv_results_df: pd.DataFrame, export_dir: str):
        """
        Dumps the randomized search history to CSV.
        """
        os.makedirs(export_dir, exist_ok=True)
        csv_path = os.path.join(export_dir, 'xgboost_tuning_history.csv')
        cv_results_df.to_csv(csv_path, index=False)
        return csv_path
