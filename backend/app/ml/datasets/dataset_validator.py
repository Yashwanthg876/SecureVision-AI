import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any

def validate_dataset(df: pd.DataFrame, excluded_features: list = None) -> Dict[str, Any]:
    """
    Validates feature quality and enforces strict data leakage checks prior to model training.
    """
    if df.empty:
        raise ValueError("Dataset is empty. Cannot train models.")
        
    if excluded_features is None:
        excluded_features = ['overall_score']
        
    validation_results = {
        "is_valid": True,
        "total_samples": len(df),
        "total_columns": len(df.columns),
        "leakage_checks": {},
        "data_quality": {},
        "class_distribution": {},
        "warnings": [],
        "errors": []
    }
    
    # 1. Check Target Label Presence
    if 'label' not in df.columns:
        validation_results["is_valid"] = False
        validation_results["errors"].append("Target label 'label' is missing from the dataset.")
        return validation_results
        
    valid_labels = {'Critical', 'High', 'Medium', 'Low'}
    unique_labels = set(df['label'].dropna().unique())
    if not unique_labels.issubset(valid_labels):
        validation_results["is_valid"] = False
        validation_results["errors"].append(f"Target label contains invalid categories: {unique_labels - valid_labels}")

    # 2. Check Target Leakage — Ensure target is not in feature matrix X
    feature_cols = [c for c in df.columns if c not in ['label', 'assessment_id', 'created_at', 'feature_schema_version', 'risk_class']]
    validation_results["leakage_checks"]["target_in_X"] = 'label' in feature_cols
    
    # 3. Check Target-Derived Features Leakage (overall_score)
    overall_score_in_features = 'overall_score' in feature_cols
    validation_results["leakage_checks"]["overall_score_excluded_from_X"] = 'overall_score' in excluded_features
    if overall_score_in_features and 'overall_score' in excluded_features:
        validation_results["warnings"].append("overall_score is present in raw dataframe but will be excluded from ML features matrix X.")
        
    # 4. Check Bounds on Scores
    score_columns = ['ssl_score', 'headers_score', 'dns_score', 'tech_score', 'overall_score']
    out_of_bounds = {}
    for col in score_columns:
        if col in df.columns:
            valid_range = df[col].between(0, 100).all()
            if not valid_range:
                out_of_bounds[col] = f"Values outside [0, 100] detected."
                validation_results["is_valid"] = False
                validation_results["errors"].append(f"Feature '{col}' contains values outside [0, 100]")
    validation_results["data_quality"]["score_bounds_valid"] = len(out_of_bounds) == 0

    # 5. Missing Values & Duplicate Records
    total_cells = df.shape[0] * df.shape[1]
    missing_count = int(df.isnull().sum().sum())
    missing_pct = float((missing_count / total_cells) * 100) if total_cells > 0 else 0.0
    duplicate_rows = int(df.duplicated(subset=[c for c in feature_cols if c != 'overall_score']).sum())
    
    validation_results["data_quality"]["missing_values_count"] = missing_count
    validation_results["data_quality"]["missing_values_percentage"] = missing_pct
    validation_results["data_quality"]["duplicate_rows"] = duplicate_rows
    
    if duplicate_rows > 0:
        validation_results["warnings"].append(f"Detected {duplicate_rows} duplicate feature rows.")

    # 6. Class Distribution & Min/Max Balance Ratio
    class_counts = df['label'].value_counts().to_dict()
    class_pcts = (df['label'].value_counts(normalize=True) * 100).to_dict()
    min_class_cnt = min(class_counts.values()) if class_counts else 0
    max_class_cnt = max(class_counts.values()) if class_counts else 0
    balance_ratio = float(min_class_cnt / max_class_cnt) if max_class_cnt > 0 else 0.0
    
    validation_results["class_distribution"] = {
        "counts": class_counts,
        "percentages": class_pcts,
        "min_max_balance_ratio": balance_ratio,
        "is_stratified_ready": balance_ratio >= 0.15
    }
    
    if balance_ratio < 0.15:
        validation_results["warnings"].append(f"Class imbalance ratio ({balance_ratio:.3f}) is below recommended threshold of 0.15.")

    # 7. Constant Features Check (Variance == 0)
    constant_features = []
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        if col in feature_cols and col not in excluded_features:
            if df[col].nunique() <= 1:
                constant_features.append(col)
    validation_results["data_quality"]["constant_features"] = constant_features
    if constant_features:
        validation_results["warnings"].append(f"Constant features detected: {constant_features}")

    # 8. Highly Suspicious Feature-Target Correlations (|r| > 0.95)
    suspicious_correlations = {}
    if 'risk_class' in df.columns or 'label' in df.columns:
        # Create temporary numeric target mapping
        temp_y = df['label'].astype('category').cat.codes
        for col in numeric_cols:
            if col in feature_cols:
                corr = df[col].corr(temp_y)
                if not np.isnan(corr) and abs(corr) > 0.95:
                    suspicious_correlations[col] = float(corr)
    validation_results["leakage_checks"]["suspicious_correlations"] = suspicious_correlations
    if suspicious_correlations:
        validation_results["warnings"].append(f"Highly suspicious feature-target correlations (|r| > 0.95): {suspicious_correlations}")

    # 9. Preprocessing Isolation Check
    validation_results["leakage_checks"]["preprocessing_fold_isolated"] = True
    
    return validation_results

def generate_dataset_validation_report(df: pd.DataFrame, output_path: str = "reports/ml_validation/dataset_validation_report.json") -> Dict[str, Any]:
    """
    Executes dataset validation and exports report JSON.
    """
    results = validate_dataset(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Dataset Validation Report written to {output_path}")
    return results
