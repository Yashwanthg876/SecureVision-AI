import sys
import os
import numpy as np
import torch

# Ensure backend path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import app.models
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.ml.trend_prediction.sequence_builder import SequenceBuilder
from app.ml.trend_prediction.lstm.trainer import LSTMTrainer
from app.ml.trend_prediction.trend_service import TrendService
from app.ml.trend_prediction.trend_visualization import TrendVisualizer

def run_trend_baseline():
    print("--- 1. Trend Intelligence Pipeline Initialization ---")
    db = SessionLocal()
    
    # 1. Build Sequences
    print("Building sequences...")
    builder = SequenceBuilder(db, sequence_length=7)
    X, y = builder.build_training_tensors()
    
    print(f"Generated {len(X)} sequences of shape {X.shape}")
    
    # 2. Train LSTM
    print("\n--- 2. Training LSTM Forecaster ---")
    trainer = LSTMTrainer(sequence_length=7, num_features=5)
    
    # Use same data for val in this prototype
    metadata = trainer.train(X, y, X, y)
    
    # 3. Save Model to Registry
    trainer.save(version="1.0")
    
    print("\n--- 3. Testing Trend Service & Inference ---")
    service = TrendService(builder)
    
    # Let's test inference on a dummy website ID (or just the first sequence if no ID)
    test_seq = X[0:1] # shape (1, 7, 5)
    
    preds, lowers, uppers = service.predictor.predict(test_seq, horizon=30, num_mc_samples=20)
    
    print("\n--- 4. Generating Visualization Reports ---")
    visualizer = TrendVisualizer()
    plot_path = visualizer.generate_forecast_chart(test_seq[0], preds, lowers, uppers)
    print(f"Confidence Interval Forecast generated at: {plot_path}")
    
    print("\n--- Done! Phase 6E Trend Engine Established ---")

if __name__ == "__main__":
    run_trend_baseline()
