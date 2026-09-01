# SPRINT 5E: ML DATASET VALIDATION & LEAKAGE REMEDIATION SUMMARY

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
| **1** | **Logistic Regression** | 0.5850 ± 0.0239 | 0.5844 ± 0.0232 | 0.5850 ± 0.0239 | 0.5772 ± 0.0271 | **0.8275 ± 0.0156** |
| **2** | **XGBoost** | 0.5850 ± 0.0261 | 0.5963 ± 0.0315 | 0.5850 ± 0.0261 | 0.5841 ± 0.0285 | **0.8142 ± 0.0091** |
| **3** | **Random Forest** | 0.5238 ± 0.0430 | 0.5209 ± 0.0469 | 0.5238 ± 0.0430 | 0.5193 ± 0.0448 | **0.7697 ± 0.0165** |
| **4** | **Extra Trees** | 0.4938 ± 0.0293 | 0.5002 ± 0.0394 | 0.4938 ± 0.0293 | 0.4927 ± 0.0324 | **0.7427 ± 0.0100** |
| **5** | **Decision Tree** | 0.4612 ± 0.0305 | 0.4559 ± 0.0336 | 0.4612 ± 0.0305 | 0.4559 ± 0.0301 | **0.6494 ± 0.0173** |

---

## 8. Best-Performing Model & Empirical Promotion
- **Empirical Winner**: **Logistic Regression**
- **Metrics**: ROC-AUC = **0.8275**, F1 Score = **0.5772**, Accuracy = **0.5850**
- **Registry Update**: `backend/app/ml/models/registry.json` updated with `Logistic Regression` as production version `1.0`.

---

## 9. Limitations & Reproducibility Information
- **Limitations**: Synthetic dataset generated with Gaussian noise. Validation on real production assessment logs is recommended for deployment.
- **Python**: `3.11.9`
- **scikit-learn**: `1.9.0`
- **XGBoost**: `3.2.0`
- **Random Seeds**: Dataset = `42`, Train/Test Split = `42`, Cross-Validation = `42`.
