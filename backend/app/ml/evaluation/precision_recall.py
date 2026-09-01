import matplotlib.pyplot as plt # type: ignore
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.preprocessing import label_binarize
import numpy as np

def plot_precision_recall_curve(y_true: np.ndarray, y_prob: np.ndarray, n_classes: int, save_path: str = None):
    """
    Generates and optionally saves Precision-Recall curve.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if n_classes == 2:
        if len(y_prob.shape) == 2:
            y_prob = y_prob[:, 1]
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        ap = average_precision_score(y_true, y_prob)
        ax.plot(recall, precision, lw=2, label=f'PR curve (AP = {ap:.2f})')
    else:
        y_test_bin = label_binarize(y_true, classes=np.arange(n_classes))
        for i in range(n_classes):
            precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_prob[:, i])
            ap = average_precision_score(y_test_bin[:, i], y_prob[:, i])
            ax.plot(recall, precision, lw=2, label=f'Class {i} (AP = {ap:.2f})')
            
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_title('Precision-Recall Curve')
    ax.legend(loc="lower left")
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()
