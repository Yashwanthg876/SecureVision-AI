import os
import json
from datetime import datetime
from typing import List, Dict, Any

class ModelRegistryManager:
    """
    Manages the centralized model registry.
    Tracks production models, candidates, and deployment history.
    """
    def __init__(self, registry_path: str = None, forecast_registry_path: str = None):
        self.registry_path = registry_path or os.path.join(os.path.dirname(__file__), 'registry.json')
        self.forecast_registry_path = forecast_registry_path or os.path.join(os.path.dirname(__file__), 'forecast_registry.json')
            
        self._initialize_registry()
        
    def _initialize_registry(self):
        initial_state = {
            "production_model": None,
            "production_version": None,
            "candidate_models": [],
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }
        if not os.path.exists(self.registry_path):
            self._save(initial_state, self.registry_path)
            
        if not os.path.exists(self.forecast_registry_path):
            self._save(initial_state, self.forecast_registry_path)
            
    def _load(self, path: str = None) -> Dict[str, Any]:
        target_path = path or self.registry_path
        with open(target_path, 'r') as f:
            return json.load(f)
            
    def _save(self, data: Dict[str, Any], path: str = None):
        target_path = path or self.registry_path
        with open(target_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    def promote_to_production(self, model_name: str, version: str):
        registry = self._load()
        self._promote(registry, model_name, version)
        self._save(registry)
        
    def add_candidate(self, model_name: str):
        registry = self._load()
        self._add_candidate(registry, model_name)
        self._save(registry)

    def promote_forecast_to_production(self, model_name: str, version: str):
        registry = self._load(self.forecast_registry_path)
        self._promote(registry, model_name, version)
        self._save(registry, self.forecast_registry_path)
        
    def add_forecast_candidate(self, model_name: str):
        registry = self._load(self.forecast_registry_path)
        self._add_candidate(registry, model_name)
        self._save(registry, self.forecast_registry_path)

    def _promote(self, registry: Dict[str, Any], model_name: str, version: str):
        current_prod = registry.get("production_model")
        if current_prod and current_prod not in registry["candidate_models"]:
            registry["candidate_models"].append(current_prod)
            
        registry["production_model"] = model_name
        registry["production_version"] = version
        registry["last_updated"] = datetime.utcnow().isoformat()
        
        if model_name in registry["candidate_models"]:
            registry["candidate_models"].remove(model_name)
            
    def _add_candidate(self, registry: Dict[str, Any], model_name: str):
        if model_name not in registry["candidate_models"] and registry.get("production_model") != model_name:
            registry["candidate_models"].append(model_name)
            registry["last_updated"] = datetime.utcnow().isoformat()
