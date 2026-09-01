# SECUREVISION AI — ML EXPERIMENT AUDIT SUMMARY

## Executive Summary
This document reports the empirical audit of the Machine Learning subsystem for **SecureVision AI**. All data, configurations, and results documented herein represent strictly verified evidence extracted directly from the execution of the existing codebase.

---

## Audit Requirements Checklist & Findings

### A. Dataset Source
- **Primary Source**: Synthetic / Stimulated data.
- **Generation Mechanism**: Generated dynamically via `generate_mock_data(db, n_samples=100)` in `backend/app/ml/run_models.py` because the initial database (`backend/securevision.db`) contained zero (`0`) assessment records.
- **Storage Location**: SQLite database table `assessments` in `backend/securevision.db`.

### B. Number of Samples
- **Total Samples Available**: **100 assessment records**.
- **Train Set Size**: **80 samples** (80% stratified split).
- **Test Set Size**: **20 samples** (20% stratified split).

### C. Number of Features
- **Raw Features Before Encoding**: **17 features** (`WebsiteFeaturesV1` dataclass).
- **Features After Encoding**: **17 encoded columns** (7 numerical scaled via `StandardScaler`, 7 boolean imputed via `SimpleImputer`, 3 categorical encoded via `OneHotEncoder`).

#### Feature Breakdown:
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
17. `overall_score` (numerical)

### D. Class Distribution
- **Target Label**: `risk_level` (`label` column in dataframe).
- **Target Categories**: 4 classes (`Critical`, `High`, `Medium`, `Low`).
- **Class Breakdown**:
  - `Medium`: **34 samples** (34.0%)
  - `High`: **32 samples** (32.0%)
  - `Low`: **26 samples** (26.0%)
  - `Critical`: **8 samples** (8.0%)
- **Imbalance Ratio (min/max)**: 0.235 (Critical vs Medium).

### E. Models Evaluated
All 5 requested models were implemented, executed, and benchmarked:
1. **Logistic Regression** (`app.ml.models.logistic_regression.model.create_logistic_regression`)
2. **Decision Tree** (`app.ml.models.decision_tree.model.create_decision_tree`)
3. **Random Forest** (`sklearn.ensemble.RandomForestClassifier` via `RandomForestTrainer`)
4. **Extra Trees** (`sklearn.ensemble.ExtraTreesClassifier` via `ExtraTreesTrainer`)
5. **XGBoost** (`xgboost.XGBClassifier` via `XGBoostTrainer` with `XGBoostTuner`)

### F. Cross-Validation Configuration
- **Scheme**: 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`).
- **Split Location**: Executed on the 80 training samples (64 train / 16 val per fold).
- **Random State**: Global random seed set to `42`.

---

## G. Performance of Every Model (5-Fold Stratified CV)

| Model | Accuracy (Mean ± Std) [Min - Max] | Precision (Mean ± Std) [Min - Max] | Recall (Mean ± Std) [Min - Max] | F1 Score (Mean ± Std) [Min - Max] | ROC-AUC (Mean ± Std) [Min - Max] |
|---|---|---|---|---|---|
| **Decision Tree** | **1.0000 ± 0.0000** [1.0000 - 1.0000] | **1.0000 ± 0.0000** [1.0000 - 1.0000] | **1.0000 ± 0.0000** [1.0000 - 1.0000] | **1.0000 ± 0.0000** [1.0000 - 1.0000] | **1.0000 ± 0.0000** [1.0000 - 1.0000] |
| **XGBoost** | **0.9875 ± 0.0250** [0.9375 - 1.0000] | **0.9896 ± 0.0208** [0.9479 - 1.0000] | **0.9875 ± 0.0250** [0.9375 - 1.0000] | **0.9872 ± 0.0256** [0.9359 - 1.0000] | **1.0000 ± 0.0000** [1.0000 - 1.0000] |
| **Random Forest** | **0.9500 ± 0.0729** [0.8125 - 1.0000] | **0.9512 ± 0.0752** [0.8058 - 1.0000] | **0.9500 ± 0.0729** [0.8125 - 1.0000] | **0.9484 ± 0.0759** [0.8045 - 1.0000] | **0.9920 ± 0.0133** [0.9659 - 1.0000] |
| **Extra Trees** | **0.8625 ± 0.1000** [0.7500 - 1.0000] | **0.8503 ± 0.1311** [0.6583 - 1.0000] | **0.8625 ± 0.1000** [0.7500 - 1.0000] | **0.8459 ± 0.1178** [0.6995 - 1.0000] | **0.9812 ± 0.0218** [0.9403 - 1.0000] |
| **Logistic Regression** | **0.7875 ± 0.0637** [0.6875 - 0.8750] | **0.8221 ± 0.0837** [0.6719 - 0.9107] | **0.7875 ± 0.0637** [0.6875 - 0.8750] | **0.7775 ± 0.0677** [0.6696 - 0.8698] | **0.9522 ± 0.0327** [0.9170 - 0.9943] |

---

## H. Best-Performing Model & Promotion Status
- **Best Model**: **Decision Tree** (Rank 1).
- **Ranking Rationale**: Evaluated according to project criteria (ROC-AUC primary, F1 secondary, Precision tertiary). Both Decision Tree and XGBoost tied at ROC-AUC = 1.0000, with Decision Tree achieving F1 = 1.0000 vs XGBoost F1 = 0.9872.
- **Production Promotion**: Promoted to production version `1.0` in `backend/app/ml/models/registry.json`.

---

## I. Data Origin (Synthetic vs Real)
- **Status**: **100% Synthetic / Stimulated Data**.
- **Evidence**: The active SQLite database (`backend/securevision.db`) contained zero real assessment records. Execution triggered the fallback function `generate_mock_data()` which populates 100 synthetic mock assessments with randomly generated score ranges. No real website assessment records exist in the current database.

---

## J. Limitations and Data Leakage Concerns

> [!WARNING]
> **Critical Audit Finding: Data Leakage & Synthetic Label Derivation**
> The current experimental benchmark results must NOT be published in an IEEE paper as representative of real-world model accuracy due to the following structural limitations:

1. **Synthetic Label Derivation Leakage**:
   In `generate_mock_data()`, target labels (`risk_level`) are assigned using a deterministic step function directly on `overall_score`:
   ```python
   risk = "Critical" if score < 40 else "High" if score < 60 else "Medium" if score < 80 else "Low"
   ```
   Because `overall_score` is simultaneously included as an unmasked numerical feature in the input vector (`WebsiteFeaturesV1`), tree-based classifiers (Decision Tree, XGBoost, Random Forest) can achieve trivial 100% accuracy by simply learning the threshold splits on `overall_score`.

2. **Preprocessing Data Leakage**:
   In `MLFeatureEncoder.fit_transform(df)` (`backend/app/ml/encoders/feature_encoder.py`), `fit_transform` is invoked on the full dataset before `split_dataset()` creates train/test splits. Consequently, `StandardScaler` (means and standard deviations), `SimpleImputer` (median values), and `OneHotEncoder` are fitted using statistics from both training and test data combined.

3. **Sample Volume Constraint**:
   The entire dataset consists of only 100 synthetic instances. Cross-validation folds contain only 16 validation samples each, resulting in high variance and unrepresentative statistical distributions.

---
