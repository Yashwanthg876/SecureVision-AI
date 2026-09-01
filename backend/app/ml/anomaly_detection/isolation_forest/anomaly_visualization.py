import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any

class AnomalyVisualizer:
    """
    Generates reports and charts for Isolation Forest anomaly detection.
    """
    def __init__(self):
        self.reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'anomaly'))
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_score_distribution(self, scores: np.ndarray, metadata: Dict[str, Any]):
        """
        Plots the histogram of anomaly scores with severity boundaries.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(scores, bins=50, color='teal', alpha=0.7)
        
        # Add boundary lines
        stats = metadata.get("score_distribution", {})
        p10 = stats.get("percentile_10")
        p5 = stats.get("percentile_5")
        
        if p10:
            ax.axvline(x=p10, color='orange', linestyle='--', label=f'Suspicious Boundary (P10)')
        if p5:
            ax.axvline(x=p5, color='red', linestyle='--', label=f'Critical Anomaly Boundary (P5)')
            
        ax.set_title('Isolation Forest Score Distribution')
        ax.set_xlabel('Anomaly Score (Lower = More Anomalous)')
        ax.set_ylabel('Frequency')
        ax.legend()
        
        plot_path = os.path.join(self.reports_dir, "score_distribution.png")
        fig.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        return plot_path
