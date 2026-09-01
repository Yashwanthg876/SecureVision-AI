import os
import json
import numpy as np
from typing import List, Dict
from app.ml.explainability.shap_engine import SHAPEngine
from app.ml.explainability.feature_mapper import FeatureMapper

class GlobalExplainer:
    """
    Computes and aggregates global model explainability metrics.
    """
    def __init__(self):
        self.engine = SHAPEngine()
        self.reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'shap'))
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_global_report(self, background_dataset: np.ndarray, feature_names: List[str]):
        """
        Computes SHAP across a large validation dataset to determine model-wide behavior.
        Generates global_shap_report.json.
        """
        explainer, model_version, _ = self.engine._initialize_explainer()
        
        shap_values = explainer.shap_values(background_dataset)
        
        # Handle multiclass vs binary shape
        if isinstance(shap_values, list):
            # For simplicity in global reporting, we can average the absolute impacts across all classes
            # or just take the sum of absolute impacts.
            # shap_values is a list of arrays (num_samples, num_features)
            mean_abs_shap = np.zeros(shap_values[0].shape[1])
            for class_shap in shap_values:
                mean_abs_shap += np.abs(class_shap).mean(axis=0)
            mean_abs_shap /= len(shap_values)
        else:
            if shap_values.ndim == 3:
                # (num_samples, num_features, num_classes)
                mean_abs_shap = np.abs(shap_values).mean(axis=(0, 2))
            else:
                mean_abs_shap = np.abs(shap_values).mean(axis=0)
                
        # Map features
        global_impacts = {}
        for idx, raw_feat in enumerate(feature_names):
            readable, _ = FeatureMapper.map_feature(raw_feat)
            impact = float(mean_abs_shap[idx])
            # If the readable name already exists, aggregate impact (e.g. one-hot encoded groups)
            global_impacts[readable] = global_impacts.get(readable, 0.0) + impact
            
        # Sort
        sorted_impacts = dict(sorted(global_impacts.items(), key=lambda item: item[1], reverse=True))
        
        report = {
            "model_version": model_version,
            "top_20_features": dict(list(sorted_impacts.items())[:20]),
            "all_features": sorted_impacts,
            "num_samples_evaluated": len(background_dataset)
        }
        
        report_path = os.path.join(self.reports_dir, "global_shap_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
            
        return report_path
