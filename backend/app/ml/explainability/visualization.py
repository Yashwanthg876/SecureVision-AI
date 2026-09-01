import os
import shap
import matplotlib.pyplot as plt
import numpy as np
from typing import List

class SHAPVisualizer:
    """
    Generates publication-quality SHAP visualizations for reporting.
    """
    def __init__(self):
        self.reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'shap'))
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_summary_plot(self, shap_values: np.ndarray, feature_data: np.ndarray, feature_names: List[str]):
        """
        Creates a global SHAP summary plot.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Handle multiclass for summary plot
        if isinstance(shap_values, list):
            # If it's a list, just plot the first class for now or plot a bar chart
            shap.summary_plot(shap_values, feature_data, feature_names=feature_names, show=False, plot_type="bar")
        else:
            shap.summary_plot(shap_values, feature_data, feature_names=feature_names, show=False)
            
        plot_path = os.path.join(self.reports_dir, "shap_summary_plot.png")
        plt.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        return plot_path
