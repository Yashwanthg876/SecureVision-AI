import sys
import os
import numpy as np

# Ensure backend path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.ml.datasets.dataset_builder import DatasetBuilder
from app.ml.anomaly_detection.isolation_forest.trainer import IsolationForestTrainer
from app.ml.anomaly_detection.isolation_forest.anomaly_visualization import AnomalyVisualizer
from app.models.assessment import Assessment
import app.models

def run_anomaly_baseline():
    print("--- 1. Anomaly Detection Pipeline Initialization ---")
    db = SessionLocal()
    
    count = db.query(Assessment).count()
    if count < 20:
        print("Not enough data to train Isolation Forest. Please run risk models baseline first.")
        return
        
    builder = DatasetBuilder(db)
    X, y, encoder = builder.get_training_dataset(print_stats=True)
    feature_names = encoder.get_feature_names_out()
    
    print("\n--- 2. Training Isolation Forest ---")
    trainer = IsolationForestTrainer(schema_version="1.0")
    metadata = trainer.train(X, feature_names)
    
    print("\n--- 3. Generating Visualization Reports ---")
    visualizer = AnomalyVisualizer()
    scores = trainer.model.decision_function(X)
    plot_path = visualizer.generate_score_distribution(scores, metadata)
    print(f"Anomaly Score Distribution generated at: {plot_path}")
    
    print("\n--- Done! Phase 6D Anomaly Engine Established ---")

if __name__ == "__main__":
    run_anomaly_baseline()
