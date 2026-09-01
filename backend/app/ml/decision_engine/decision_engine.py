import uuid
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

from app.ml.decision_engine.model_loader import ModelLoader
from app.ml.decision_engine.voting import VotingEngine
from app.ml.decision_engine.confidence import ConfidenceEngine
from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from app.ml.config.decision_engine_config import DEFAULT_VOTING_STRATEGY

class DecisionEngine:
    """
    Central orchestration layer for Machine Learning inference.
    Aggregates predictions from all registered health-checked models.
    """
    def __init__(self, class_labels: List[str]):
        """
        :param class_labels: The ordered list of class labels (e.g. ['Critical', 'High', 'Medium', 'Low'])
                             that correspond to the model's output probabilities indices.
        """
        self.model_loader = ModelLoader()
        self.class_labels = class_labels
        
    def _log_audit(self, prediction: UnifiedPrediction):
        """
        Persists a Prediction Audit Log containing timestamps, outputs, confidence, strategy, and final prediction.
        """
        import os
        import json
        
        audit_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'experiments', 'audits'))
        os.makedirs(audit_dir, exist_ok=True)
        
        audit_path = os.path.join(audit_dir, f"{prediction.prediction_id}.json")
        
        audit_record = prediction.model_dump()
        audit_record["timestamp"] = datetime.utcnow().isoformat()
        
        with open(audit_path, 'w') as f:
            json.dump(audit_record, f, indent=4)
            
    def predict(self, feature_vector: np.ndarray, strategy: str = DEFAULT_VOTING_STRATEGY) -> UnifiedPrediction:
        """
        Executes inference across all active models and returns a UnifiedPrediction.
        """
        models = self.model_loader.get_active_models()
        
        if not models:
            raise RuntimeError("Decision Engine Failed: No active models available for inference.")
            
        individual_preds = {}
        model_probs = {}
        model_versions = {}
        
        for model_name, model in models.items():
            try:
                # Assuming feature_vector is 2D: shape (1, n_features)
                pred = model.predict(feature_vector)[0]
                individual_preds[model_name] = pred
                
                prob = model.predict_proba(feature_vector)
                if prob is not None:
                    model_probs[model_name] = prob
                    
                model_versions[model_name] = model.get_metadata().get("model_version", "unknown")
            except Exception as e:
                print(f"Model {model_name} failed during inference: {str(e)}")
                # Graceful skip
                continue
                
        if not individual_preds:
            raise RuntimeError("Decision Engine Failed: All models failed during inference.")
            
        # 1. Voting
        final_prediction = ""
        probabilities = {}
        
        if strategy == "Majority Voting":
            final_prediction = VotingEngine.majority_voting(individual_preds)
            # Rough probabilities if we don't have true probability averaging
            if model_probs:
                _, probabilities = VotingEngine.probability_averaging(model_probs, self.class_labels)
        
        elif strategy == "Weighted Voting":
            final_prediction = VotingEngine.weighted_voting(individual_preds, models)
            if model_probs:
                _, probabilities = VotingEngine.probability_averaging(model_probs, self.class_labels)
                
        elif strategy == "Probability Averaging":
            if not model_probs:
                # Fallback if no models support predict_proba
                final_prediction = VotingEngine.majority_voting(individual_preds)
            else:
                final_prediction, probabilities = VotingEngine.probability_averaging(model_probs, self.class_labels)
        else:
            raise ValueError(f"Unknown voting strategy: {strategy}")
            
        # 2. Confidence
        confidence_profile = ConfidenceEngine.compute_confidence(final_prediction, individual_preds, probabilities)
        
        # 3. Schema Construction
        unified = UnifiedPrediction(
            prediction_id=str(uuid.uuid4()),
            prediction=final_prediction,
            confidence=confidence_profile["confidence"],
            confidence_level=confidence_profile["confidence_level"],
            agreement_score=confidence_profile["agreement_score"],
            models_agreeing=confidence_profile["models_agreeing"],
            total_models=confidence_profile["total_models"],
            strategy=strategy,
            individual_predictions=individual_preds,
            probabilities=probabilities,
            model_versions=model_versions,
            explanation=None
        )
        
        # 4. Audit Log
        self._log_audit(unified)
        
        return unified
