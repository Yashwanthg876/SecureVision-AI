import numpy as np
from app.ml.training.model_persistence import load_model

class ExtraTreesPredictor:
    """
    Predictor for Extra Trees Model.
    """
    def __init__(self, version: str = "1.0"):
        self.model = load_model("Extra Trees", version)
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
        
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)
