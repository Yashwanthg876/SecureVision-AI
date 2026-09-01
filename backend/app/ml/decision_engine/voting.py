import numpy as np
from typing import Dict, List, Tuple, Any
from app.ml.decision_engine.model_loader import BasePredictionModel
from app.ml.config.decision_engine_config import DYNAMIC_WEIGHT_METRIC

class VotingEngine:
    """
    Implements ensemble voting strategies.
    """
    
    @staticmethod
    def majority_voting(predictions: Dict[str, str]) -> str:
        """
        Determines the final prediction based on the majority of predicted labels.
        """
        from collections import Counter
        counts = Counter(predictions.values())
        return counts.most_common(1)[0][0]

    @staticmethod
    def weighted_voting(predictions: Dict[str, str], models: Dict[str, BasePredictionModel]) -> str:
        """
        Assigns dynamic weights derived from model metadata.
        """
        score_tally = {}
        total_weight = 0.0
        
        for model_name, pred_label in predictions.items():
            model = models.get(model_name)
            weight = 1.0 # Default fallback
            
            if model:
                metadata = model.get_metadata()
                # Get dynamic metric, fallback to 1.0 if not found
                weight = float(metadata.get(DYNAMIC_WEIGHT_METRIC, 1.0))
                
            total_weight += weight
            score_tally[pred_label] = score_tally.get(pred_label, 0.0) + weight
            
        # Return label with highest weighted score
        best_label = max(score_tally, key=score_tally.get)
        return best_label

    @staticmethod
    def probability_averaging(model_probs: Dict[str, np.ndarray], classes: List[str]) -> Tuple[str, Dict[str, float]]:
        """
        Averages prediction probabilities across all participating models.
        Returns the winning label and the averaged probability dictionary.
        """
        if not model_probs:
            raise ValueError("No probabilities provided for averaging")
            
        # Assuming all models output probabilities in the same class order
        all_probs = list(model_probs.values())
        avg_probs = np.mean(all_probs, axis=0) # Shape: (1, num_classes) or (num_classes,)
        
        # Flatten if needed
        if avg_probs.ndim > 1:
            avg_probs = avg_probs[0]
            
        prob_dict = {classes[i]: float(avg_probs[i]) for i in range(len(classes))}
        
        best_class = classes[np.argmax(avg_probs)]
        
        return best_class, prob_dict
