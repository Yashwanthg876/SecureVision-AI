from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any, Tuple

class BaseForecaster(ABC):
    """
    Abstract base class for all forecasting models (LSTM, GRU, Transformers).
    Ensures a consistent API for the Trend Intelligence Engine.
    """
    
    @abstractmethod
    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        """
        Trains the forecasting model.
        Returns:
            metadata dictionary (e.g. MAE, RMSE, MAPE, R2, epochs)
        """
        pass
        
    @abstractmethod
    def predict(self, sequence: np.ndarray, horizon: int = 1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generates a forecast for the given horizon.
        Args:
            sequence: Historical time-series data
            horizon: Number of steps ahead to predict (e.g., 1 for Next Assessment, 7 for Next 7 Days)
        Returns:
            Tuple containing:
            - predictions: The forecasted values
            - lower_bound: Lower confidence interval
            - upper_bound: Upper confidence interval
        """
        pass
        
    @abstractmethod
    def save(self, version: str):
        """
        Persists the trained model to disk.
        """
        pass
        
    @abstractmethod
    def load(self, version: str):
        """
        Loads a pre-trained model from disk.
        """
        pass
