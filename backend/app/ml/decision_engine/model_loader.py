import os
import json
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
from app.ml.training.model_persistence import load_model
from app.ml.models.registry_manager import ModelRegistryManager

class BasePredictionModel(ABC):
    """
    Common interface that every classifier must implement to be used by the Decision Engine.
    """
    @abstractmethod
    def predict(self, X: Any) -> Any:
        pass
        
    @abstractmethod
    def predict_proba(self, X: Any) -> Any:
        pass
        
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass

class GenericPredictionModel(BasePredictionModel):
    """
    Wrapper for standard Scikit-Learn/Joblib models to conform to the BasePredictionModel interface.
    """
    def __init__(self, model_name: str, model: Any, metadata: Dict[str, Any]):
        self.model_name = model_name
        self._model = model
        self._metadata = metadata
        
    def predict(self, X: Any) -> Any:
        return self._model.predict(X)
        
    def predict_proba(self, X: Any) -> Any:
        if hasattr(self._model, "predict_proba"):
            return self._model.predict_proba(X)
        return None
        
    def get_metadata(self) -> Dict[str, Any]:
        return self._metadata

class ModelLoader:
    """
    Dynamically loads registered models and performs health checks.
    """
    def __init__(self):
        self.registry = ModelRegistryManager()
        self.metadata_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'metadata'))
        # In-memory cache
        self._cached_models: Dict[str, BasePredictionModel] = {}
        
    def _read_metadata(self, model_name: str) -> Optional[Dict[str, Any]]:
        safe_name = model_name.replace(" ", "_").lower()
        meta_path = os.path.join(self.metadata_dir, f"{safe_name}_metadata.json")
        if not os.path.exists(meta_path):
            return None
        with open(meta_path, 'r') as f:
            return json.load(f)
            
    def _health_check(self, model_name: str, expected_schema: str = "1.0") -> Optional[Dict[str, Any]]:
        """
        Validates model files, metadata, and feature schema versions.
        """
        metadata = self._read_metadata(model_name)
        if not metadata:
            print(f"Health Check Failed: Missing metadata for {model_name}")
            return None
            
        if metadata.get("feature_schema_version") != expected_schema:
            print(f"Health Check Failed: Schema mismatch for {model_name}. Expected {expected_schema}, got {metadata.get('feature_schema_version')}")
            return None
            
        # We assume load_model will throw FileNotFoundError if joblib is missing
        return metadata

    def get_active_models(self, force_reload: bool = False, expected_schema: str = "1.0") -> Dict[str, BasePredictionModel]:
        """
        Reads the registry and returns all healthy production and candidate models.
        """
        if self._cached_models and not force_reload:
            return self._cached_models
            
        registry_data = self.registry._load()
        models_to_load = []
        if registry_data.get("production_model"):
            models_to_load.append(registry_data["production_model"])
            
        for cand in registry_data.get("candidate_models", []):
            if cand not in models_to_load:
                models_to_load.append(cand)
                
        loaded = {}
        for model_name in models_to_load:
            metadata = self._health_check(model_name, expected_schema)
            if not metadata:
                continue # Skip gracefully
                
            try:
                # Load joblib model
                version = metadata.get("model_version", "1.0")
                raw_model = load_model(model_name, version)
                loaded[model_name] = GenericPredictionModel(model_name, raw_model, metadata)
            except Exception as e:
                print(f"Failed to load {model_name}: {str(e)}")
                # Skip gracefully
                
        self._cached_models = loaded
        return loaded
