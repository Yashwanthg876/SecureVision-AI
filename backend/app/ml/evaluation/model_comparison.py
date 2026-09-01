import pandas as pd
from typing import Dict, Any

def compare_models(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Takes a dictionary of model results (e.g. from K-Fold) and returns a DataFrame 
    for easy tabular comparison of their metrics.
    """
    records = []
    for model_name, metrics in results.items():
        metrics["model_name"] = model_name
        records.append(metrics)
        
    df = pd.DataFrame(records)
    # Reorder columns to put model_name first
    cols = ["model_name"] + [c for c in df.columns if c != "model_name"]
    return df[cols]
