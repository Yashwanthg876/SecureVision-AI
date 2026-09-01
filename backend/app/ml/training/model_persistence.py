import os
import joblib
from typing import Any

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved')

def save_model(model: Any, model_name: str, version: str = "v1"):
    """
    Saves a trained model to disk using joblib.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    safe_name = model_name.replace(" ", "_").lower()
    file_path = os.path.join(MODELS_DIR, f"{safe_name}_{version}.joblib")
    
    joblib.dump(model, file_path)
    return file_path

def load_model(model_name: str, version: str = "v1") -> Any:
    """
    Loads a trained model from disk.
    """
    safe_name = model_name.replace(" ", "_").lower()
    file_path = os.path.join(MODELS_DIR, f"{safe_name}_{version}.joblib")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Model not found at {file_path}")
        
    return joblib.load(file_path)
