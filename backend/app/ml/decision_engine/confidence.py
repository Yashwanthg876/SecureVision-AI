from typing import Dict, List, Any
from app.ml.config.decision_engine_config import CONFIDENCE_THRESHOLDS

class ConfidenceEngine:
    """
    Computes rigorous confidence metrics and model agreement scores.
    """
    
    @staticmethod
    def calculate_agreement(final_prediction: str, individual_predictions: Dict[str, str]) -> float:
        """
        Calculates the ratio of models that agree with the final prediction.
        """
        if not individual_predictions:
            return 0.0
            
        agreeing_models = sum(1 for pred in individual_predictions.values() if pred == final_prediction)
        return float(agreeing_models) / len(individual_predictions)
        
    @staticmethod
    def map_human_confidence(confidence_score: float) -> str:
        """
        Maps a 0.0 to 1.0 confidence score into a human-readable string based on thresholds.
        """
        for label, threshold in CONFIDENCE_THRESHOLDS.items():
            if confidence_score >= threshold:
                return label
        return "Very Low"

    @staticmethod
    def compute_confidence(
        final_prediction: str, 
        individual_predictions: Dict[str, str], 
        probabilities: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generates full confidence profile for a prediction.
        """
        agreement_score = ConfidenceEngine.calculate_agreement(final_prediction, individual_predictions)
        models_agreeing = sum(1 for pred in individual_predictions.values() if pred == final_prediction)
        
        # Base confidence is the averaged probability of the chosen class
        prob_confidence = probabilities.get(final_prediction, 0.0)
        
        # A simple robust metric: average the probability with the agreement score
        # so if 1 model is hyper-confident but the rest disagree, confidence drops.
        blended_confidence = (prob_confidence + agreement_score) / 2.0
        
        human_readable = ConfidenceEngine.map_human_confidence(blended_confidence)
        
        return {
            "confidence": blended_confidence,
            "confidence_level": human_readable,
            "agreement_score": agreement_score,
            "models_agreeing": models_agreeing,
            "total_models": len(individual_predictions)
        }
