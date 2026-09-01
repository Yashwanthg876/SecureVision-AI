import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.trend_prediction.base_forecaster import BaseForecaster
from app.ml.trend_prediction.lstm.model import LSTMForecaster
from app.ml.config.model_config import LSTM_CONFIG
from app.ml.models.registry_manager import ModelRegistryManager

class LSTMTrainer(BaseForecaster):
    """
    PyTorch training loop for the LSTM model.
    Implements BaseForecaster interface.
    """
    def __init__(self, sequence_length: int = 7, num_features: int = 5):
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
        
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config["learning_rate"])
        
    def _mean_absolute_percentage_error(self, y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        # Avoid division by zero
        mask = y_true != 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray = None, y_val: np.ndarray = None) -> Dict[str, Any]:
        print("Training LSTM Trend Intelligence Engine...")
        start_time = time.time()
        
        X_tensor = torch.tensor(X_train, dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(y_train, dtype=torch.float32).to(self.device)
        
        epochs = self.config["epochs"]
        batch_size = self.config["batch_size"]
        
        self.model.train()
        
        # Simple training loop (no DataLoader for simplicity in prototype)
        dataset_size = len(X_train)
        
        for epoch in range(epochs):
            permutation = torch.randperm(dataset_size)
            
            for i in range(0, dataset_size, batch_size):
                indices = permutation[i:i+batch_size]
                batch_x, batch_y = X_tensor[indices], y_tensor[indices]
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
                
            if (epoch+1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
                
        training_duration = time.time() - start_time
        
        # Calculate Validation Metrics
        self.model.eval()
        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy()
            
        mae = mean_absolute_error(y_train, preds)
        rmse = np.sqrt(mean_squared_error(y_train, preds))
        r2 = r2_score(y_train, preds)
        mape = self._mean_absolute_percentage_error(y_train, preds)
        
        metadata = {
            "model_architecture": "LSTM",
            "sequence_length": self.sequence_length,
            "hidden_size": self.config["hidden_size"],
            "num_layers": self.config["num_layers"],
            "dropout": self.config["dropout"],
            "epochs": epochs,
            "batch_size": batch_size,
            "training_duration_s": training_duration,
            "metrics": {
                "MAE": float(mae),
                "RMSE": float(rmse),
                "MAPE": float(mape),
                "R2": float(r2)
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        print(f"LSTM trained in {training_duration:.2f}s | RMSE: {rmse:.2f}")
        return metadata
        
    def predict(self, sequence: np.ndarray, horizon: int = 1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Defined in predictor.py instead for clean separation of concerns, 
        # but required by abstract base class.
        pass
        
    def save(self, version: str):
        models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'joblib_models'))
        os.makedirs(models_dir, exist_ok=True)
        path = os.path.join(models_dir, f"lstm_{version}.pt")
        torch.save(self.model.state_dict(), path)
        
        # Register in Forecast Registry
        registry = ModelRegistryManager()
        registry.add_forecast_candidate("lstm")
        registry.promote_forecast_to_production("lstm", version)
        
    def load(self, version: str):
        models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'joblib_models'))
        path = os.path.join(models_dir, f"lstm_{version}.pt")
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.eval()
