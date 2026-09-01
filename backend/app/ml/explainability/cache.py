from typing import Any, Optional

class SHAPCache:
    """
    Singleton cache to persist the SHAP Explainer and Background Data
    in memory. Prevents expensive TreeExplainer initializations on every request.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SHAPCache, cls).__new__(cls)
            cls._instance.explainer = None
            cls._instance.model_version = None
            cls._instance.feature_names = None
        return cls._instance
        
    def get_explainer(self) -> Optional[Any]:
        return self.explainer
        
    def set_explainer(self, explainer: Any, model_version: str, feature_names: list):
        self.explainer = explainer
        self.model_version = model_version
        self.feature_names = feature_names
        
    def is_valid(self, requested_version: str) -> bool:
        return self.explainer is not None and self.model_version == requested_version
