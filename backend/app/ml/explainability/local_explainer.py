import numpy as np
from typing import List, Dict, Any, Tuple
from app.ml.explainability.feature_mapper import FeatureMapper
from app.ml.explainability.explanation_schema import FeatureContribution

class LocalExplainer:
    """
    Processes raw SHAP values for a single prediction and generates
    structured local explanations (Top Features, Category Contributions).
    """
    
    @staticmethod
    def extract_contributions(
        shap_values_instance: np.ndarray, 
        feature_names: List[str],
        top_n: int = 5
    ) -> Tuple[List[FeatureContribution], List[FeatureContribution], Dict[str, float]]:
        """
        Extracts top positive/negative features and aggregates by category.
        """
        positive_features = []
        negative_features = []
        category_impacts = {}
        
        # Build list of (feature_name, impact)
        contributions = list(zip(feature_names, shap_values_instance))
        
        for raw_feat, impact in contributions:
            if abs(impact) < 1e-6:
                continue
                
            readable_name, category = FeatureMapper.map_feature(raw_feature)
            
            # Aggregate category impact
            category_impacts[category] = category_impacts.get(category, 0.0) + abs(float(impact))
            
            fc = FeatureContribution(feature=readable_name, impact=float(impact))
            
            if impact > 0:
                positive_features.append(fc)
            else:
                negative_features.append(fc)
                
        # Sort by impact magnitude
        positive_features.sort(key=lambda x: x.impact, reverse=True)
        negative_features.sort(key=lambda x: x.impact) # Most negative first
        
        return positive_features[:top_n], negative_features[:top_n], category_impacts
