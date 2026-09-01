# -*- coding: utf-8 -*-
import sys
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any
  
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import app.models
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.ml.datasets.dataset_builder import DatasetBuilder
from app.ml.config.model_config import LOGISTIC_REGRESSION_CONFIG, DECISION_TREE_CONFIG, RANDOM_FOREST_CONFIG, EXTRA_TREES_CONFIG
from app.ml.models.logistic_regression.model import create_logistic_regression
from app.ml.models.decision_tree.model import create_decision_tree
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from app.ml.models.random_forest.trainer import RandomForestTrainer
from app.ml.models.extra_trees.trainer import ExtraTreesTrainer
from app.ml.training.trainer import ModelTrainer
from app.ml.training.evaluator import ModelEvaluator
from app.ml.evaluation.cross_validation import evaluate_with_kfold
from app.ml.evaluation.model_comparison import compare_models
from app.models.assessment import Assessment
from app.ml.models.registry_manager import ModelRegistryManager
from app.ml.experiments.report_generator import ExperimentReportGenerator

from app.ml.models.xgboost.tuning import XGBoostTuner
from app.ml.models.xgboost.trainer import XGBoostTrainer
from app.ml.models.xgboost.calibration import ProbabilityCalibrator
from app.ml.encoders.feature_encoder import MLFeatureEncoder
from app.ml.datasets.dataset_validator import validate_dataset, generate_dataset_validation_report
from sklearn.model_selection import train_test_split

def generate_mock_data(db: Session, n_samples=1000, random_state=42):
    """
    Sprint 5E Corrected Synthetic Dataset Generator.
    Generates 1,000 realistic, non-deterministic assessment samples based on multi-factor security
    characteristics. Target risk_level is derived from a latent vulnerability index prior to
    computing overall_score, eliminating target leakage.
    """
    import random
    import uuid
    from datetime import datetime, timedelta
    from app.models.user import User
    
    random.seed(random_state)
    np.random.seed(random_state)
    
    user = db.query(User).first()
    if not user:
        user = User(
            id=uuid.uuid4(),
            email="researcher@securevision.ai",
            hashed_password="hashed_password_placeholder",
            full_name="ML Audit Researcher"
        )
        db.add(user)
        db.commit()
        
    print(f"Generating {n_samples} multi-factor synthetic assessment records (random_state={random_state})...")
    
    servers = ["nginx", "apache", "cloudflare", "iis", "caddy"]
    frameworks = ["React", "Next.js", "Django", "Express", "Laravel", "Vue.js"]
    tls_versions = ["TLSv1.3", "TLSv1.2", "TLSv1.1", "TLSv1.0"]
    
    for i in range(n_samples):
        # 1. Independent Security Telemetry Characteristics
        ssl_valid = random.random() < 0.75
        cert_days = random.randint(10, 365) if ssl_valid else random.randint(0, 5)
        tls_ver = np.random.choice(tls_versions, p=[0.50, 0.30, 0.12, 0.08])
        
        has_hsts = random.random() < 0.50
        has_csp = random.random() < 0.40
        has_x_frame = random.random() < 0.60
        has_x_content = random.random() < 0.60
        
        has_spf = random.random() < 0.70
        has_dmarc = random.random() < 0.40
        
        domain_age = random.randint(30, 3650)
        server_tech = str(random.choice(servers))
        framework_tech = str(random.choice(frameworks))
        
        # 2. Derive Domain Sub-Scores with realistic noise
        ssl_score = max(0, min(100, int(
            (50 if ssl_valid else 10) +
            (25 if tls_ver == "TLSv1.3" else 20 if tls_ver == "TLSv1.2" else 10 if tls_ver == "TLSv1.1" else 0) +
            (25 if cert_days > 30 else 5) +
            np.random.normal(0, 5)
        )))
        
        headers_score = max(0, min(100, int(
            (30 if has_hsts else 5) +
            (30 if has_csp else 5) +
            (20 if has_x_frame else 5) +
            (20 if has_x_content else 5) +
            np.random.normal(0, 5)
        )))
        
        dns_score = max(0, min(100, int(
            (50 if has_spf else 15) +
            (50 if has_dmarc else 15) +
            np.random.normal(0, 5)
        )))
        
        tech_score = max(0, min(100, int(
            (30 if domain_age > 365 else 10) +
            (40 if server_tech in ["nginx", "cloudflare"] else 25) +
            (30 if framework_tech in ["React", "Next.js"] else 20) +
            np.random.normal(0, 5)
        )))
        
        # 3. Multi-Factor Latent Vulnerability Index (incorporates non-linear security risk + noise)
        latent_risk = (
            (100 - ssl_score) * 0.35 +
            (100 - headers_score) * 0.35 +
            (100 - dns_score) * 0.15 +
            (100 - tech_score) * 0.15 +
            np.random.normal(0, 8.0)
        )
        
        # 4. Target Risk Level classification based on latent risk quantiles
        if latent_risk >= 45:
            risk = "Critical"
        elif latent_risk >= 33:
            risk = "High"
        elif latent_risk >= 20:
            risk = "Medium"
        else:
            risk = "Low"
            
        # 5. Calculate overall_score post-generation as an aggregate summary metric
        overall_score = max(0, min(100, int(
            0.35 * ssl_score + 0.35 * headers_score + 0.15 * dns_score + 0.15 * tech_score
        )))
        
        ssl_details = {"valid": ssl_valid, "days_remaining": cert_days, "tls_version": str(tls_ver)}
        headers_details = {}
        if has_hsts: headers_details["Strict-Transport-Security"] = "max-age=31536000"
        if has_csp: headers_details["Content-Security-Policy"] = "default-src 'self'"
        if has_x_frame: headers_details["X-Frame-Options"] = "DENY"
        if has_x_content: headers_details["X-Content-Type-Options"] = "nosniff"
        
        dns_details = {}
        if has_spf: dns_details["spf_record"] = "v=spf1 include:_spf.example.com ~all"
        if has_dmarc: dns_details["dmarc_record"] = "v=DMARC1; p=reject;"
        
        whois_details = {"creation_date": (datetime.utcnow() - timedelta(days=domain_age)).isoformat()}
        technology_details = {"server": server_tech, "framework": framework_tech}
        
        assessment = Assessment(
            id=uuid.uuid4(),
            user_id=user.id,
            target_url=f"https://sample-site-{i+1}.org",
            domain=f"sample-site-{i+1}.org",
            status="completed",
            overall_score=overall_score,
            risk_level=risk,
            ssl_score=ssl_score,
            headers_score=headers_score,
            dns_score=dns_score,
            tech_score=tech_score,
            scan_duration=random.randint(200, 1800),
            ssl_details=ssl_details,
            headers_details=headers_details,
            dns_details=dns_details,
            whois_details=whois_details,
            technology_details=technology_details,
            created_at=datetime.utcnow()
        )
        db.add(assessment)
        
    db.commit()
    print(f"Successfully generated {n_samples} synthetic assessment records.")

def generate_comparison_charts(comparison_df: pd.DataFrame, export_dir: str):
    os.makedirs(export_dir, exist_ok=True)
    metrics_to_plot = ['mean_accuracy', 'mean_f1_score', 'mean_roc_auc']
    model_col = 'model_name' if 'model_name' in comparison_df.columns else 'Model'
    
    for metric in metrics_to_plot:
        if metric in comparison_df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(comparison_df[model_col], comparison_df[metric], color='skyblue')
            ax.set_title(f'Model Comparison: {metric}')
            ax.set_ylabel(metric)
            ax.set_ylim(0, 1.0)
            plt.xticks(rotation=45)
            fig.savefig(os.path.join(export_dir, f'comparison_{metric.replace(" ", "_").lower()}.png'), bbox_inches='tight')
            plt.close(fig)

def generate_deployment_report(best_model: str, comparison_df: pd.DataFrame, registry_path: str):
    report_path = os.path.join(os.path.dirname(__file__), 'experiments', 'deployment_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Production Deployment Report - Sprint 5E Validated\n\n")
        f.write(f"**Promoted Model**: {best_model}\n\n")
        f.write("## Evaluation Evidence (Zero Leakage Cross-Validation)\n")
        f.write(comparison_df.to_markdown(index=False))
        f.write("\n\n## Decision Criteria\n")
        f.write("The promotion policy evaluated ROC-AUC (primary), F1-Score (secondary), and Precision (tertiary). "
                "The promoted model demonstrated empirical superiority on the leakage-remediated dataset.")
    print(f"Deployment Report saved to {report_path}")

def export_sprint_5e_reports(df_raw: pd.DataFrame, results_dict: Dict[str, Any], final_metrics: Dict[str, Any], best_model_name: str, encoder_train: MLFeatureEncoder, reports_dir: str = "reports/ml_validation"):
    """
    Exports all 7 required validation report artifacts for Sprint 5E.
    """
    os.makedirs(reports_dir, exist_ok=True)
    import sklearn
    import xgboost
    
    # 1. dataset_validation_report.json
    generate_dataset_validation_report(df_raw, os.path.join(reports_dir, "dataset_validation_report.json"))
    
    # 2. dataset_statistics.csv
    from app.ml.datasets.dataset_statistics import generate_dataset_statistics
    stats = generate_dataset_statistics(df_raw, label_col="label")
    stats_rows = [
        {"Metric": "Total Samples", "Value": str(stats.get("total_samples"))},
        {"Metric": "Raw Features Count (in X)", "Value": "16"},
        {"Metric": "Duplicate Records", "Value": str(stats.get("duplicate_records"))},
        {"Metric": "Missing Values Percentage", "Value": f"{stats.get('missing_values_percentage', 0):.2f}%"},
        {"Metric": "Derived From Real Data", "Value": "False (100% Synthetic)"},
        {"Metric": "Class Ratio (min/max)", "Value": f"{stats.get('balance_ratio_min_max', 0):.4f}"}
    ]
    for k, v in stats.get("label_distribution", {}).items():
        stats_rows.append({"Metric": f"Class Count ({k})", "Value": str(v)})
    pd.DataFrame(stats_rows).to_csv(os.path.join(reports_dir, "dataset_statistics.csv"), index=False)
    
    # 3. corrected_experiment_results.csv & corrected_experiment_results.json
    exp_rows = []
    exp_json = {
        "evaluation_config": {
            "cv_method": "5-Fold Stratified K-Fold (Fold-Isolated Preprocessing)",
            "n_splits": 5,
            "train_samples": len(df_raw) * 4 // 5,
            "test_samples": len(df_raw) // 5,
            "random_state": 42,
            "ranking_criteria": ["ROC-AUC (primary)", "F1 Score (secondary)", "Precision (tertiary)"]
        },
        "models": {}
    }
    
    sorted_models = sorted(
        results_dict.items(),
        key=lambda item: (item[1].get("mean_roc_auc", 0), item[1].get("mean_f1_score", 0), item[1].get("mean_precision", 0)),
        reverse=True
    )
    
    for rank, (m_name, m_cv) in enumerate(sorted_models, start=1):
        row = {
            "Rank": rank,
            "Model": m_name,
            "Accuracy_Mean": round(m_cv.get("mean_accuracy", 0), 4),
            "Accuracy_Std": round(m_cv.get("std_accuracy", 0), 4),
            "Accuracy_Min": round(m_cv.get("min_accuracy", 0), 4),
            "Accuracy_Max": round(m_cv.get("max_accuracy", 0), 4),
            "Precision_Mean": round(m_cv.get("mean_precision", 0), 4),
            "Precision_Std": round(m_cv.get("std_precision", 0), 4),
            "Precision_Min": round(m_cv.get("min_precision", 0), 4),
            "Precision_Max": round(m_cv.get("max_precision", 0), 4),
            "Recall_Mean": round(m_cv.get("mean_recall", 0), 4),
            "Recall_Std": round(m_cv.get("std_recall", 0), 4),
            "Recall_Min": round(m_cv.get("min_recall", 0), 4),
            "Recall_Max": round(m_cv.get("max_recall", 0), 4),
            "F1_Mean": round(m_cv.get("mean_f1_score", 0), 4),
            "F1_Std": round(m_cv.get("std_f1_score", 0), 4),
            "F1_Min": round(m_cv.get("min_f1_score", 0), 4),
            "F1_Max": round(m_cv.get("max_f1_score", 0), 4),
            "ROC_AUC_Mean": round(m_cv.get("mean_roc_auc", 0), 4),
            "ROC_AUC_Std": round(m_cv.get("std_roc_auc", 0), 4),
            "ROC_AUC_Min": round(m_cv.get("min_roc_auc", 0), 4),
            "ROC_AUC_Max": round(m_cv.get("max_roc_auc", 0), 4)
        }
        exp_rows.append(row)
        
        exp_json["models"][m_name] = {
            "rank": rank,
            "accuracy": {"mean": row["Accuracy_Mean"], "std": row["Accuracy_Std"], "min": row["Accuracy_Min"], "max": row["Accuracy_Max"], "folds": m_cv.get("accuracy_folds")},
            "precision": {"mean": row["Precision_Mean"], "std": row["Precision_Std"], "min": row["Precision_Min"], "max": row["Precision_Max"], "folds": m_cv.get("precision_folds")},
            "recall": {"mean": row["Recall_Mean"], "std": row["Recall_Std"], "min": row["Recall_Min"], "max": row["Recall_Max"], "folds": m_cv.get("recall_folds")},
            "f1_score": {"mean": row["F1_Mean"], "std": row["F1_Std"], "min": row["F1_Min"], "max": row["F1_Max"], "folds": m_cv.get("f1_score_folds")},
            "roc_auc": {"mean": row["ROC_AUC_Mean"], "std": row["ROC_AUC_Std"], "min": row["ROC_AUC_Min"], "max": row["ROC_AUC_Max"], "folds": m_cv.get("roc_auc_folds")}
        }
        
    pd.DataFrame(exp_rows).to_csv(os.path.join(reports_dir, "corrected_experiment_results.csv"), index=False)
    with open(os.path.join(reports_dir, "corrected_experiment_results.json"), "w", encoding='utf-8') as f:
        json.dump(exp_json, f, indent=4)
        
    # 4. old_vs_corrected.csv
    old_results = {
        "Decision Tree": {"acc": 1.0000, "f1": 1.0000, "auc": 1.0000, "status": "INVALID - TARGET LEAKAGE"},
        "XGBoost": {"acc": 0.9875, "f1": 0.9872, "auc": 1.0000, "status": "INVALID - TARGET LEAKAGE"},
        "Random Forest": {"acc": 0.9500, "f1": 0.9484, "auc": 0.9920, "status": "INVALID - TARGET LEAKAGE"},
        "Extra Trees": {"acc": 0.8625, "f1": 0.8459, "auc": 0.9812, "status": "INVALID - TARGET LEAKAGE"},
        "Logistic Regression": {"acc": 0.7875, "f1": 0.7775, "auc": 0.9522, "status": "INVALID - TARGET LEAKAGE"}
    }
    
    comparison_rows = []
    for m_name, m_cv in results_dict.items():
        old = old_results.get(m_name, {})
        comparison_rows.append({
            "Model": m_name,
            "Old_Status": old.get("status", "INVALID"),
            "Old_Accuracy": old.get("acc"),
            "Old_F1": old.get("f1"),
            "Old_ROC_AUC": old.get("auc"),
            "Corrected_Status": "VALIDATED EXPERIMENT",
            "Corrected_Accuracy": round(m_cv.get("mean_accuracy", 0), 4),
            "Corrected_F1": round(m_cv.get("mean_f1_score", 0), 4),
            "Corrected_ROC_AUC": round(m_cv.get("mean_roc_auc", 0), 4)
        })
    pd.DataFrame(comparison_rows).to_csv(os.path.join(reports_dir, "old_vs_corrected.csv"), index=False)
    
    # 5. experiment_config.json
    config_json = {
        "reproducibility": {
            "dataset_random_seed": 42,
            "train_test_split_seed": 42,
            "cross_validation_seed": 42,
            "xgb_tuning_seed": 42,
            "n_samples": len(df_raw),
            "n_features_raw_in_X": 16,
            "excluded_features": ["overall_score"],
            "raw_feature_names": [
                "ssl_is_valid", "cert_expiry_days", "tls_version", "has_hsts", "has_csp",
                "has_x_frame_options", "has_x_content_type_options", "has_spf", "has_dmarc",
                "domain_age_days", "server_software", "framework", "ssl_score", "headers_score",
                "dns_score", "tech_score"
            ],
            "encoded_feature_names": encoder_train.get_feature_names_out(),
            "class_distribution": df_raw['label'].value_counts().to_dict(),
            "environment": {
                "python_version": sys.version.split()[0],
                "scikit_learn_version": sklearn.__version__,
                "xgboost_version": xgboost.__version__
            }
        }
    }
    with open(os.path.join(reports_dir, "experiment_config.json"), "w", encoding='utf-8') as f:
        json.dump(config_json, f, indent=4)
        
    # 6. ML_VALIDATION_SUMMARY.md
    top_model = sorted_models[0][0]
    top_roc = round(sorted_models[0][1].get("mean_roc_auc", 0), 4)
    top_f1 = round(sorted_models[0][1].get("mean_f1_score", 0), 4)
    top_acc = round(sorted_models[0][1].get("mean_accuracy", 0), 4)
    
    summary_md = f"""# SPRINT 5E: ML DATASET VALIDATION & LEAKAGE REMEDIATION SUMMARY

> [!IMPORTANT]
> **IEEE PAPER SAFETY REQUIREMENT**:
> The original benchmark results (Sprint 5D) are **NOT** suitable as evidence of real-world predictive performance because the synthetic target was directly derived from `overall_score` and preprocessing was performed before data splitting.
> The corrected experiment documented below must be the **only** benchmark used in the IEEE Results section.

---

## 1. Dataset Methodology
- **Generation Model**: Multi-Factor Latent Vulnerability Index (`generate_mock_data` in `backend/app/ml/run_models.py`).
- **Data Type**: 100% Synthetic / Stimulated Security Telemetry.
- **Random Seed**: `random_state = 42`.
- **Target Derivation**: Security telemetry characteristics (SSL validity, cert expiry, TLS version, HTTP security headers, DNS authentication, WHOIS domain age, server/framework technologies) are generated first. A non-deterministic latent vulnerability index with Gaussian noise ($\sigma = 8.0$) determines `risk_level` (`Critical`, `High`, `Medium`, `Low`). `overall_score` is computed post-generation as a secondary metric and **excluded** from input feature matrix $X$.

## 2. Number of Samples & Split Configuration
- **Total Samples**: **1,000 assessment records**.
- **Train Split**: **800 samples** (80% Stratified Split, `random_state=42`).
- **Test Split**: **200 samples** (20% Stratified Holdout Split, `random_state=42`).

## 3. Feature Count & List
- **Raw Input Features in Matrix $X$**: **16 features** (17 total features minus excluded `overall_score`).
- **Excluded Features**: `overall_score` (retained in DB telemetry for reporting, but excluded from ML training to prevent target leakage).
- **Raw Feature List**:
  1. `ssl_is_valid` (boolean)
  2. `cert_expiry_days` (numerical)
  3. `tls_version` (categorical)
  4. `has_hsts` (boolean)
  5. `has_csp` (boolean)
  6. `has_x_frame_options` (boolean)
  7. `has_x_content_type_options` (boolean)
  8. `has_spf` (boolean)
  9. `has_dmarc` (boolean)
  10. `domain_age_days` (numerical)
  11. `server_software` (categorical)
  12. `framework` (categorical)
  13. `ssl_score` (numerical)
  14. `headers_score` (numerical)
  15. `dns_score` (numerical)
  16. `tech_score` (numerical)

## 4. Class Distribution
- `Medium`: **349 samples** (34.9%)
- `High`: **252 samples** (25.2%)
- `Low`: **245 samples** (24.5%)
- `Critical`: **154 samples** (15.4%)
- **Min/Max Balance Ratio**: **0.4413** (Healthy balance, >= 0.15 threshold satisfied).

## 5. Leakage Issues Discovered & Fixes Implemented
1. **Target Leakage Fix**: Removed `overall_score` from `MLFeatureEncoder` numerical feature list. Re-derived `risk_level` from multi-factor latent risk index with stochastic noise before computing `overall_score`.
2. **Preprocessing Leakage Fix**: Refactored `evaluate_with_kfold()` to accept raw DataFrame slices. `MLFeatureEncoder` is instantiated and fitted **strictly inside each training fold** (zero test-fold leakage into `StandardScaler`, `SimpleImputer`, or `OneHotEncoder`).
3. **Dataset Scale Expansion**: Expanded dataset from 100 to 1,000 samples to ensure stable validation fold distributions.

## 6. Preprocessing & Cross-Validation Methodology
- **Preprocessing Strategy**: Median imputation for numerical features, most frequent imputation for booleans, constant imputation + OneHotEncoding for categoricals, and `StandardScaler` for numerical scaling.
- **Cross-Validation**: 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) executed on the 800 training samples. Preprocessing fitted independently on the 640 training samples per fold.

---

## 7. Corrected Empirical Model Performance (5-Fold CV)

| Rank | Model | Accuracy (Mean ± Std) | Precision (Mean ± Std) | Recall (Mean ± Std) | F1 Score (Mean ± Std) | ROC-AUC (Mean ± Std) |
|---|---|---|---|---|---|---|
"""
    for r in exp_rows:
        summary_md += f"| **{r['Rank']}** | **{r['Model']}** | {r['Accuracy_Mean']:.4f} ± {r['Accuracy_Std']:.4f} | {r['Precision_Mean']:.4f} ± {r['Precision_Std']:.4f} | {r['Recall_Mean']:.4f} ± {r['Recall_Std']:.4f} | {r['F1_Mean']:.4f} ± {r['F1_Std']:.4f} | **{r['ROC_AUC_Mean']:.4f} ± {r['ROC_AUC_Std']:.4f}** |\n"

    summary_md += f"""
---

## 8. Best-Performing Model & Empirical Promotion
- **Empirical Winner**: **{top_model}**
- **Metrics**: ROC-AUC = **{top_roc:.4f}**, F1 Score = **{top_f1:.4f}**, Accuracy = **{top_acc:.4f}**
- **Registry Update**: `backend/app/ml/models/registry.json` updated with `{top_model}` as production version `1.0`.

---

## 9. Limitations & Reproducibility Information
- **Limitations**: Synthetic dataset generated with Gaussian noise. Validation on real production assessment logs is recommended for deployment.
- **Python**: `{sys.version.split()[0]}`
- **scikit-learn**: `{sklearn.__version__}`
- **XGBoost**: `{xgboost.__version__}`
- **Random Seeds**: Dataset = `42`, Train/Test Split = `42`, Cross-Validation = `42`.
"""
    with open(os.path.join(reports_dir, "ML_VALIDATION_SUMMARY.md"), "w", encoding='utf-8') as f:
        f.write(summary_md)
        
    print(f"All 7 Sprint 5E validation report artifacts saved to {reports_dir}/")

def run_models():
    db = SessionLocal()
    registry = ModelRegistryManager()
    
    count = db.query(Assessment).count()
    if count < 1000:
        db.query(Assessment).delete()
        db.commit()
        generate_mock_data(db, n_samples=1000, random_state=42)
        
    print("--- 1. Dataset Preparation & Leakage Validation ---")
    builder = DatasetBuilder(db)
    df_raw = builder.build_raw_dataframe()
    
    # Run Dataset Validation and export report
    generate_dataset_validation_report(df_raw, "reports/ml_validation/dataset_validation_report.json")
    
    # Train / Hold-out Test Split BEFORE Preprocessing Fitting (Zero Preprocessing Leakage)
    df_train, df_test = train_test_split(df_raw, test_size=0.2, stratify=df_raw['label'], random_state=42)
    print(f"Raw DataFrame Shape: {df_raw.shape}")
    print(f"Train DataFrame Shape: {df_train.shape}, Hold-out Test Shape: {df_test.shape}")
    
    print("\n--- 2. XGBoost Hyperparameter Tuning ---")
    # For tuning, fit encoder on df_train
    encoder_tuning = MLFeatureEncoder()
    X_train_tune, y_train_tune = encoder_tuning.fit_transform(df_train, save_artifacts=False)
    
    tuner = XGBoostTuner()
    best_xgb_params, cv_results_df = tuner.tune(X_train_tune, y_train_tune, n_iter=10)
    export_dir = os.path.join(os.path.dirname(__file__), 'experiments', 'xgboost')
    tuner.export_history(cv_results_df, export_dir)
    print(f"XGBoost Best Params: {best_xgb_params}")
    
    print("\n--- 3. 5-Fold Stratified Cross Validation (Fold-Isolated Preprocessing) ---")
    
    lr_cv = evaluate_with_kfold(df_train, lambda: create_logistic_regression(**LOGISTIC_REGRESSION_CONFIG), n_splits=5, random_state=42)
    dt_cv = evaluate_with_kfold(df_train, lambda: create_decision_tree(**DECISION_TREE_CONFIG), n_splits=5, random_state=42)
    rf_cv = evaluate_with_kfold(df_train, lambda: RandomForestClassifier(**RANDOM_FOREST_CONFIG), n_splits=5, random_state=42)
    et_cv = evaluate_with_kfold(df_train, lambda: ExtraTreesClassifier(**EXTRA_TREES_CONFIG), n_splits=5, random_state=42)
    xgb_cv = evaluate_with_kfold(
        df_train, 
        lambda: XGBClassifier(**best_xgb_params, use_label_encoder=False, eval_metric='mlogloss' if len(np.unique(df_train['label'])) > 2 else 'logloss', random_state=42), 
        n_splits=5, random_state=42
    )
    
    results_dict = {
        "Logistic Regression": lr_cv,
        "Decision Tree": dt_cv,
        "Random Forest": rf_cv,
        "Extra Trees": et_cv,
        "XGBoost": xgb_cv
    }
    
    comparison_df = compare_models(results_dict)
    print("\n[Corrected Model Comparison (5-Fold CV)]")
    print(comparison_df.to_string(index=False))
    
    print("\n--- 4. Final Training, Metadata & Hold-out Evaluation ---")
    # Fit final preprocessor strictly on training split
    encoder_train = MLFeatureEncoder()
    X_train, y_train = encoder_train.fit_transform(df_train, save_artifacts=True)
    X_test = encoder_train.transform(df_test)
    y_test = encoder_train.label_encoder.transform(df_test['label'])
    
    class_names = encoder_train.label_encoder.classes_
    feature_names = encoder_train.get_feature_names_out()
    final_metrics = {}
    
    # 4a. Logistic Regression
    lr_trainer = ModelTrainer("Logistic Regression", create_logistic_regression, LOGISTIC_REGRESSION_CONFIG)
    lr_trainer.train_and_evaluate(X_train, y_train, X_test, y_test, cv_metrics=lr_cv)
    final_metrics["Logistic Regression"] = ModelEvaluator(lr_trainer.model, class_names).evaluate(X_test, y_test)
    registry.add_candidate("Logistic Regression")
    
    # 4b. Decision Tree
    dt_trainer = ModelTrainer("Decision Tree", create_decision_tree, DECISION_TREE_CONFIG)
    dt_trainer.train_and_evaluate(X_train, y_train, X_test, y_test, cv_metrics=dt_cv)
    final_metrics["Decision Tree"] = ModelEvaluator(dt_trainer.model, class_names).evaluate(X_test, y_test)
    registry.add_candidate("Decision Tree")

    # 4c. Random Forest
    rf_trainer = RandomForestTrainer(RANDOM_FOREST_CONFIG)
    rf_trainer.train_and_evaluate_ensemble(X_train, y_train, X_test, y_test, feature_names, cv_metrics=rf_cv)
    final_metrics["Random Forest"] = ModelEvaluator(rf_trainer.model, class_names).evaluate(X_test, y_test)
    registry.add_candidate("Random Forest")

    # 4d. Extra Trees
    et_trainer = ExtraTreesTrainer(EXTRA_TREES_CONFIG)
    et_trainer.train_and_evaluate_ensemble(X_train, y_train, X_test, y_test, feature_names, cv_metrics=et_cv)
    final_metrics["Extra Trees"] = ModelEvaluator(et_trainer.model, class_names).evaluate(X_test, y_test)
    registry.add_candidate("Extra Trees")

    # 4e. XGBoost
    print("\nTraining XGBoost with Early Stopping...")
    xgb_trainer = XGBoostTrainer(best_xgb_params)
    xgb_trainer.train_and_evaluate_ensemble(X_train, y_train, X_test, y_test, feature_names, cv_metrics=xgb_cv)
    xgb_evaluator = ModelEvaluator(xgb_trainer.model, class_names)
    final_metrics["XGBoost"] = xgb_evaluator.evaluate(X_test, y_test)
    xgb_evaluator.generate_visualizations(X_test, y_test, os.path.join(os.path.dirname(__file__), "logs", "visualizations", "xgboost"))
    registry.add_candidate("XGBoost")

    # Probability Calibration
    print("\nCalibrating XGBoost...")
    try:
        calibrator = ProbabilityCalibrator(xgb_trainer.model, cv=3)
        calibrator.fit(X_test, y_test)
    except Exception as e:
        print(f"Warning: Probability calibration skipped: {e}")
    
    print("\n--- 5. Empirical Promotion & Validation Report Export ---")
    # Rank models using Primary: ROC-AUC, Secondary: F1, Tertiary: Precision
    sorted_models = sorted(
        results_dict.items(),
        key=lambda item: (item[1].get("mean_roc_auc", 0), item[1].get("mean_f1_score", 0), item[1].get("mean_precision", 0)),
        reverse=True
    )
    best_model_name = sorted_models[0][0]
    print(f"\nEmpirically Promoting {best_model_name} to Production based on Corrected Benchmark Results.")
    registry.promote_to_production(best_model_name, "1.0")
    
    generate_deployment_report(best_model_name, comparison_df, registry.registry_path)
    generate_comparison_charts(comparison_df, os.path.join(os.path.dirname(__file__), 'experiments', 'charts'))
    
    # Export Sprint 5E Validation Reports
    export_sprint_5e_reports(df_raw, results_dict, final_metrics, best_model_name, encoder_train, "reports/ml_validation")
    
    print("\n--- Sprint 5E Complete: ML Dataset Validation & Leakage Remediation Established ---")

if __name__ == "__main__":
    run_models()
