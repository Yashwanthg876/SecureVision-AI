import numpy as np
from typing import List, Dict, Tuple
from app.ml.explainability.feature_mapper import FeatureMapper

class AnomalyReasonEngine:
    """
    Identifies which feature categories contributed most to an anomaly
    by comparing the assessment against global baselines.
    """
    def __init__(self, global_means: Dict[str, float] = None, global_stds: Dict[str, float] = None):
        # In a real system, these would be loaded from the training set metadata
        self.global_means = global_means or {}
        self.global_stds = global_stds or {}
        
    def determine_contributions(
        self, 
        feature_vector: np.ndarray, 
        feature_names: List[str]
    ) -> Tuple[List[str], Dict[str, float]]:
        """
        Approximates feature contribution to the anomaly by measuring z-score deviations.
        Returns Top Contributing Features and Category Scores.
        """
        vector = feature_vector.flatten()
        category_deviations = {}
        feature_deviations = []
        
        for idx, feat_val in enumerate(vector):
            feat_name = feature_names[idx]
            
            # Simple fallback if global stats aren't provided: 
            # We assume features with extreme values (e.g. 0 when normally 1, or very low scores)
            # are anomalous. For demonstration, we'll use a mock z-score approach if missing.
            mean = self.global_means.get(feat_name, 0.5)
            std = self.global_stds.get(feat_name, 0.5)
            
            # Prevent division by zero
            if std < 1e-6:
                std = 1e-6
                
            z_score = abs(feat_val - mean) / std
            
            if z_score > 1.0: # Only count significant deviations
                readable_name, category = FeatureMapper.map_feature(feat_name)
                category_deviations[category] = category_deviations.get(category, 0.0) + z_score
                feature_deviations.append((readable_name, z_score))
                
        # Sort features by deviation
        feature_deviations.sort(key=lambda x: x[1], reverse=True)
        top_features = [f[0] for f in feature_deviations[:5]]
        
        # Normalize category scores to 0-1 range for easier frontend consumption
        total_dev = sum(category_deviations.values())
        if total_dev > 0:
            for cat in category_deviations:
                category_deviations[cat] = category_deviations[cat] / total_dev
                
        return top_features, category_deviations
