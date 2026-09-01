import torch
import numpy as np
from typing import Tuple, Dict, Any

from app.ml.trend_prediction.base_forecaster import BaseForecaster
from app.ml.trend_prediction.lstm.model import LSTMForecaster
from app.ml.config.model_config import LSTM_CONFIG
from app.ml.models.registry_manager import ModelRegistryManager
import os

class LSTMPredictor(BaseForecaster):
    """
    Handles inference for the LSTM forecasting model.
    Implements Monte Carlo Dropout to generate Confidence Intervals.
    """
    def __init__(self, sequence_length: int = 7, num_features: int = 5, version: str = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.sequence_length = sequence_length
        self.num_features = num_features
        self.config = LSTM_CONFIG
        
        self.model = LSTMForecaster(
            input_size=num_features,
            hidden_size=self.config["hidden_size"],
            num_layers=self.config["num_layers"],
            output_size=num_features,
            dropout=self.config["dropout"]
        ).to(self.device)
        
        if not version:
            registry = ModelRegistryManager()
            forecast_registry = registry._load(registry.forecast_registry_path)
            version = forecast_registry.get("production_version")
            
        if version:
            self.load(version)
            
    def load(self, version: str):
        models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'joblib_models'))
        path = os.path.join(models_dir, f"lstm_{version}.pt")
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path, map_location=self.device))
        else:
            raise RuntimeError(f"LSTM model {version} not found at {path}")
            
    def save(self, version: str):
        pass # Implemented in trainer
        
    def train(self, X_train, y_train, X_val, y_val):
        pass # Implemented in trainer

    def predict(self, sequence: np.ndarray, horizon: int = 1, num_mc_samples: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Predicts future time steps.
        Args:
            sequence: shape (1, seq_len, num_features)
            horizon: Number of steps to forecast
            num_mc_samples: Number of forward passes for Monte Carlo Dropout uncertainty
        Returns:
            preds: (horizon, num_features)
            lower_bounds: (horizon, num_features)
            upper_bounds: (horizon, num_features)
        """
        # Enable dropout layers for Monte Carlo uncertainty sampling
        self.model.train() 
        
        current_seq = torch.tensor(sequence, dtype=torch.float32).to(self.device)
        
        preds_all = []
        lowers_all = []
        uppers_all = []
        
        # Autoregressive forecasting for `horizon` steps
        for step in range(horizon):
            mc_predictions = []
            
            with torch.no_grad():
                for _ in range(num_mc_samples):
                    out = self.model(current_seq) # shape: (1, num_features)
                    mc_predictions.append(out.cpu().numpy()[0])
                    
            mc_predictions = np.array(mc_predictions)
            
            # Mean prediction
            mean_pred = np.mean(mc_predictions, axis=0)
            
            # 90% Confidence Intervals
            lower_bound = np.percentile(mc_predictions, 5, axis=0)
            upper_bound = np.percentile(mc_predictions, 95, axis=0)
            
            preds_all.append(mean_pred)
            lowers_all.append(lower_bound)
            uppers_all.append(upper_bound)
            
            # Autoregressive update: append prediction to sequence, remove oldest step
            mean_pred_tensor = torch.tensor(mean_pred, dtype=torch.float32).to(self.device).unsqueeze(0).unsqueeze(0)
            current_seq = torch.cat((current_seq[:, 1:, :], mean_pred_tensor), dim=1)
            
        return np.array(preds_all), np.array(lowers_all), np.array(uppers_all)
