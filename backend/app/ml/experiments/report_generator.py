import os
import json
import pandas as pd
from typing import Dict, Any

class ExperimentReportGenerator:
    """
    Generates consolidated experiment reports across all models.
    """
    def __init__(self, reports_dir: str = None):
        if reports_dir is None:
            self.reports_dir = os.path.join(os.path.dirname(__file__), '..', 'experiments')
        else:
            self.reports_dir = reports_dir
            
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_report(self, comparison_df: pd.DataFrame, metrics_dict: Dict[str, Dict[str, Any]]):
        """
        Creates CSV and JSON summaries of the final experiment run.
        """
        csv_path = os.path.join(self.reports_dir, 'experiment_summary.csv')
        json_path = os.path.join(self.reports_dir, 'experiment_summary.json')
        
        # Save CSV
        comparison_df.to_csv(csv_path, index=False)
        
        # Identify best models
        col_acc = 'mean_accuracy' if 'mean_accuracy' in comparison_df.columns else 'Mean Accuracy'
        col_f1 = 'mean_f1_score' if 'mean_f1_score' in comparison_df.columns else 'Mean F1 Score'
        col_model = 'model_name' if 'model_name' in comparison_df.columns else 'Model'

        best_accuracy_idx = comparison_df[col_acc].idxmax()
        best_f1_idx = comparison_df[col_f1].idxmax()
        
        summary = {
            "best_performing_model_accuracy": comparison_df.iloc[best_accuracy_idx][col_model],
            "best_performing_model_f1": comparison_df.iloc[best_f1_idx][col_model],
            "model_comparison": comparison_df.to_dict(orient='records'),
            "detailed_metrics": metrics_dict
        }
        
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=4)
            
        return csv_path, json_path
