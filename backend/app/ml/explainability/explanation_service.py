import uuid
import json
import os
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

from app.ml.explainability.shap_engine import SHAPEngine
from app.ml.explainability.local_explainer import LocalExplainer
from app.ml.explainability.summary_generator import SummaryGenerator
from app.ml.explainability.explanation_schema import ExplanationSchema
from app.ml.decision_engine.prediction_schema import UnifiedPrediction

class ExplanationService:
    """
    The unified explainability API boundary.
    Coordinates SHAP generation, feature mapping, and audit logging.
    """
    def __init__(self):
        self.engine = SHAPEngine()
        self.audit_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'experiments', 'explainability_audits'))
        os.makedirs(self.audit_dir, exist_ok=True)
        
    def _log_audit(self, explanation: ExplanationSchema):
        audit_path = os.path.join(self.audit_dir, f"{explanation.explanation_id}.json")
        with open(audit_path, 'w') as f:
            json.dump(explanation.model_dump(), f, indent=4)
            
    def _map_explanation_confidence(self, prediction_confidence_level: str) -> str:
        # For now, explanation confidence tracks prediction confidence, 
        # but this could be decoupled if SHAP stability metrics are added.
        return prediction_confidence_level

    def generate_explanation(self, prediction: UnifiedPrediction, feature_vector: np.ndarray, feature_names: List[str]) -> ExplanationSchema:
        """
        Generates a full SHAP explanation for a given prediction and feature vector.
        """
        start_time = time.time()
        
        # 1. SHAP Computation
        # Extract base values and shap values
        shap_values = self.engine.explain_instance(feature_vector)
        
        # SHAP often returns a list for multiclass, or 2D array.
        # We need the 1D impact array for the specific predicted class if multiclass.
        # For simplicity, we assume we want the impact towards the predicted class.
        
        # Determine the index of the predicted class
        # (assuming we know the class labels, e.g., ["Critical", "High", "Low", "Medium"])
        # We'll use a heuristic for this prototype: if shap_values is a list, 
        # we take the impacts of the highest probability class, or the first element if binary.
        instance_shap = None
        if isinstance(shap_values, list):
            # Try to map prediction to an index
            class_order = ["Critical", "High", "Low", "Medium"]
            try:
                idx = class_order.index(prediction.prediction)
                if idx < len(shap_values):
                    instance_shap = shap_values[idx][0]
                else:
                    instance_shap = shap_values[0][0]
            except ValueError:
                instance_shap = shap_values[0][0]
        else:
            # 2D array: shape (1, num_features)
            if shap_values.ndim == 2:
                instance_shap = shap_values[0]
            elif shap_values.ndim == 3:
                # (1, num_features, num_classes)
                instance_shap = shap_values[0, :, 0] # fallback
            else:
                instance_shap = shap_values
                
        # 2. Local Extraction
        pos_features, neg_features, cat_contributions = LocalExplainer.extract_contributions(
            instance_shap, feature_names
        )
        
        # 3. Summarization
        summary = SummaryGenerator.generate_summary(prediction.prediction, pos_features, neg_features)
        
        # 4. Schema Assembly
        expl_id = str(uuid.uuid4())
        
        schema = ExplanationSchema(
            explanation_id=expl_id,
            prediction_id=prediction.prediction_id,
            prediction=prediction.prediction,
            confidence=prediction.confidence,
            explanation_confidence=self._map_explanation_confidence(prediction.confidence_level),
            top_positive_features=pos_features,
            top_negative_features=neg_features,
            category_contributions=cat_contributions,
            summary=summary,
            recommendations=[],
            model_versions=prediction.model_versions,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # 5. Audit Log
        self._log_audit(schema)
        
        latency = time.time() - start_time
        print(f"Explanation {expl_id} generated in {latency:.3f}s")
        
        return schema
