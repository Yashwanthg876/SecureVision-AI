# SecureVision AI: ML Model Lifecycle

This document defines the architectural guidelines and lifecycle for machine learning models within SecureVision AI.

## 1. Model Training Flow

1. **Feature Engineering**: Completed assessments pass through `feature_pipeline.py` which utilizes modular extractors to build numerical feature vectors.
2. **Dataset Building**: `DatasetBuilder` fetches from PostgreSQL, unwraps JSONB telemetry, flattens it, and passes it through the `MLFeatureEncoder` for scaling and one-hot encoding.
3. **Cross-Validation**: Models are first piped through a 5-Fold Stratified K-Fold harness (`evaluate_with_kfold`) to evaluate performance variance.
4. **Final Training**: The `ModelTrainer` (or `BaseEnsembleTrainer` for tree-based models) fits the final estimator on the full training split.
5. **Evaluation**: `ModelEvaluator` computes standard classification metrics and generates `matplotlib` visualizations (ROC, Precision-Recall, Confusion Matrix).

## 2. Model Persistence & Metadata Generation

Every training run automatically generates two artifacts per model:
- **Serialized Model**: Saved as `.joblib` in `backend/app/ml/models/saved/`.
- **Metadata File**: Saved as `.json` in `backend/app/ml/models/metadata/`.

**Metadata File Contents:**
- Model name & version
- Feature schema and dataset versions
- Complete dictionary of applied hyperparameters
- Train/Validation/Test split sizes
- Execution metrics (Training duration, accuracy, precision, F1, ROC-AUC)
- K-Fold metrics across all folds
- Pointer to feature importance extraction file (if ensemble)
- `scikit-learn` version

## 3. Model Registry

All model deployments are managed via a centralized registry:
`backend/app/ml/models/registry.json`

The registry tracks:
- `production_model`: The current active model serving predictions
- `production_version`: The active model's version
- `candidate_models`: List of available but inactive models
- Last updated timestamps

When a new model demonstrates superior accuracy in the benchmark, the orchestration script automatically promotes it to production in the registry.

## 4. Experiment Tracking

We utilize a dual-logging system inside `backend/app/ml/training/experiment_logger.py`:
- `experiment_summary.csv`: A lightweight, tabular ledger for quick tracking of runs over time.
- `experiment_summary.json`: A deep-dive dump of all cross-validation matrices, hyperparameters, and test evaluations.

## 5. Feature Drift Monitoring

Before predicting, incoming datasets can be passed through `FeatureDriftMonitor` (`backend/app/ml/monitoring/feature_drift.py`).
- Compares numerical features against the original training distribution (means/stds).
- Computes percentage divergence.
- Triggers dynamic severity warnings (Medium/High) if feature deviation exceeds predefined thresholds (e.g., 15%).
- Logs drifted features for downstream investigation.

## 6. Future Production Deployment Process

In future sprints, production predictions will rely entirely on the Model Registry.
The prediction service will:
1. Parse `registry.json` to identify the `production_model` string.
2. Dynamically load the associated Joblib model and its exact preprocessing pipeline.
3. Invoke the inference endpoint.

*Note: Models are never retrained automatically in production without a human-in-the-loop validation of the generated metadata and K-fold reports.*
