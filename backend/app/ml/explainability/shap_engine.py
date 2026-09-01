import time
import numpy as np
from typing import Dict, Any, Tuple
from app.ml.decision_engine.model_loader import ModelLoader
from app.ml.explainability.model_adapter import ExplainerAdapter
from app.ml.explainability.cache import SHAPCache

class SHAPEngine:
    """
    Core engine for computing SHAP values.
    Retrieves models from the registry and manages the explanation pipeline.
    """
    def __init__(self):
        self.model_loader = ModelLoader()
        self.cache = SHAPCache()
        
    def _initialize_explainer(self) -> Tuple[Any, str, list]:
        """
        Loads the production model and initializes the correct SHAP explainer.
        """
        start_time = time.time()
        
        # Load all active models, but we specifically target the production model for SHAP
        models = self.model_loader.get_active_models()
        registry_data = self.model_loader.registry._load()
        prod_model_name = registry_data.get("production_model")
        
        if not prod_model_name or prod_model_name not in models:
            raise RuntimeError("SHAP Engine Failed: No healthy production model found.")
            
        prod_model = models[prod_model_name]
        metadata = prod_model.get_metadata()
        model_version = metadata.get("model_version", "unknown")
        
        # If cache is valid, return it
        if self.cache.is_valid(model_version):
            return self.cache.get_explainer(), model_version, self.cache.feature_names
            
        # We need background data if the model isn't tree-based.
        # For this prototype, we'll assume tree-based or supply a dummy if needed.
        # Ideally, this should pull a background dataset from DatasetBuilder.
        background_data = None
        
        try:
            explainer = ExplainerAdapter.get_explainer(prod_model, background_data)
        except ValueError as e:
            # Fallback: if we absolutely need background data, we should fetch it.
            # In a production system, we'd query the DB and pass a sample here.
            raise RuntimeError(f"Failed to initialize explainer: {str(e)}")
            
        # Feature names should be provided. In our pipeline, it's not explicitly in model_loader yet,
        # but we can assume the feature pipeline will align. For now, we leave it empty if unknown
        # and rely on the explainer's internal properties if available, or pass it later.
        feature_names = []
        
        self.cache.set_explainer(explainer, model_version, feature_names)
        
        latency = time.time() - start_time
        print(f"SHAP Explainer initialized in {latency:.3f} seconds (Cache Miss)")
        
        return explainer, model_version, feature_names
        
    def explain_instance(self, feature_vector: np.ndarray) -> np.ndarray:
        """
        Computes SHAP values for a single prediction instance.
        Returns the raw SHAP values array.
        """
        explainer, _, _ = self._initialize_explainer()
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(feature_vector)
        
        # TreeExplainer might return a list of arrays (one per class) for multiclass classification
        # For simplicity, if it's a list, we return it as is and let the local explainer handle the classes.
        return shap_values
