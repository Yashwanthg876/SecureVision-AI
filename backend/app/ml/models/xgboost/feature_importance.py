import os
import json
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from xgboost import XGBClassifier

class XGBoostFeatureImportance:
    """
    Extracts and exports XGBoost-specific feature importances (Weight, Cover, Gain).
    Caches the artifacts specifically for future SHAP integration.
    """
    def __init__(self, model: XGBClassifier, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        
    def extract_all(self, export_dir: str):
        """
        Extracts all 3 types of XGBoost importance and exports them to JSON/Charts.
        """
        os.makedirs(export_dir, exist_ok=True)
        
        # XGBoost natively returns a booster which has get_score
        booster = self.model.get_booster()
        
        # Map generic 'f0', 'f1' to actual feature names
        def map_names(importance_dict: Dict[str, float]) -> Dict[str, float]:
            mapped = {}
            for k, v in importance_dict.items():
                try:
                    # k is 'f0', 'f1', etc.
                    idx = int(k[1:])
                    mapped[self.feature_names[idx]] = v
                except (ValueError, IndexError):
                    mapped[k] = v
            # Sort by descending
            return dict(sorted(mapped.items(), key=lambda item: item[1], reverse=True))

        importances = {}
        types = ['weight', 'gain', 'cover']
        
        for imp_type in types:
            try:
                scores = booster.get_score(importance_type=imp_type)
                importances[imp_type] = map_names(scores)
                
                # Save JSON for SHAP cache
                json_path = os.path.join(export_dir, f'xgboost_{imp_type}_importance.json')
                with open(json_path, 'w') as f:
                    json.dump(importances[imp_type], f, indent=4)
                    
                # Generate high-res matplotlib chart
                self._plot_importance(importances[imp_type], imp_type, export_dir)
            except Exception as e:
                print(f"Failed to extract {imp_type} importance: {str(e)}")
                
        return importances

    def _plot_importance(self, importance_dict: Dict[str, float], imp_type: str, export_dir: str):
        top_20 = dict(list(importance_dict.items())[:20])
        if not top_20:
            return
            
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(list(top_20.keys())[::-1], list(top_20.values())[::-1], color='coral')
        ax.set_xlabel(f'Importance Score ({imp_type.capitalize()})')
        ax.set_title(f'Top 20 Features - XGBoost ({imp_type.capitalize()})')
        
        plot_path = os.path.join(export_dir, f'xgboost_{imp_type}_importance.png')
        fig.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
