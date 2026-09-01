import pandas as pd
from typing import Dict, Any
import json

def generate_dataset_statistics(df: pd.DataFrame, label_col: str = "label") -> Dict[str, Any]:
    """
    Generates summary statistics for the unencoded dataset to evaluate quality and balance.
    """
    if df.empty:
        return {"error": "Empty dataset"}
        
    stats = {
        "total_samples": len(df),
        "feature_count": len(df.columns) - 1,  # minus label
        "duplicate_records": int(df.duplicated().sum()),
        "missing_values_percentage": (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
        "label_distribution": df[label_col].value_counts().to_dict() if label_col in df.columns else {}
    }
    
    # Calculate dataset balance (entropy or simple ratio)
    if stats["label_distribution"]:
        max_class = max(stats["label_distribution"].values())
        min_class = min(stats["label_distribution"].values())
        stats["balance_ratio_min_max"] = min_class / max_class if max_class > 0 else 0
        
    numeric_cols = df.select_dtypes(include=['number']).columns
    stats["numerical_ranges"] = {}
    for col in numeric_cols:
        if col != 'risk_class': # exclude encoded label if present
            stats["numerical_ranges"][col] = {
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "mean": float(df[col].mean()),
                "std": float(df[col].std())
            }
            
    return stats

def print_dataset_statistics(stats: Dict[str, Any]):
    print("--- Dataset Statistics ---")
    print(json.dumps(stats, indent=2))
    print("--------------------------")
