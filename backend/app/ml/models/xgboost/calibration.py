import numpy as np
from typing import Any
from sklearn.calibration import CalibratedClassifierCV

class ProbabilityCalibrator:
    """
    Wraps an XGBoost classifier (or any classifier) to ensure probability predictions
    are statistically calibrated. This improves the Decision Engine's Probability Averaging
    and Confidence scoring reliability.
    """
    def __init__(self, base_estimator: Any, method: str = 'sigmoid', cv: Any = 3):
        self.calibrated_model = CalibratedClassifierCV(
            estimator=base_estimator,
            method=method,
            cv=cv,
            n_jobs=-1 if cv != 'prefit' else None
        )
        
    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Fits the calibrator on the dataset.
        """
        self.calibrated_model.fit(X_train, y_train)
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.calibrated_model.predict(X)
        
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.calibrated_model.predict_proba(X)
