# SecureVision AI - Machine Learning Subsystem

This module contains the preprocessing, feature engineering, and training configurations for all predictive models within SecureVision AI.

## Architecture

The ML subsystem is modular and follows standard data science architecture:
- **`schemas/`**: Strongly typed data models representing feature sets. `FeatureVector` wraps individual domain features.
- **`features/`**: Stateless, decoupled scripts that parse raw `JSONB` blobs from PostgreSQL into usable floats/ints/bools.
- **`pipelines/`**: High-level aggregators that combine all modular features into a single `FeatureVector`.
- **`encoders/`**: Stateful scikit-learn `ColumnTransformer` pipelines that scale numerics and One-Hot-Encode categoricals. These are saved to `joblib` so that during inference we do not have data leakage.
- **`datasets/`**: Tools to query historical DB records, build `pandas.DataFrames`, split data into Train/Test subsets, and print dataset summary statistics.
- **`config/`**: Centralized hyperparameter dictionaries for algorithms (XGBoost, Random Forest, etc.) to prevent hardcoding inside training scripts.
- **`models/`**: (Future) Saved models and training scripts categorized by algorithm family.

## Typical Workflow

### 1. Training Flow
1. Instantiate `DatasetBuilder(db)` and call `get_training_dataset(print_stats=True)`.
2. Retrieve `X` (features), `y` (labels), and the fitted `MLFeatureEncoder`.
3. Pass `X, y` to `train_test_splitter.py` to get `X_train`, `X_test`, etc.
4. Load config from `model_config.py` and train the model (e.g. `XGBClassifier(**XGBOOST_CONFIG)`).
5. The `feature_encoder` automatically saves `preprocessor.joblib` and `feature_mapping.json`.

### 2. Inference Flow
1. Fetch a new `Assessment` object.
2. Build the unencoded feature dict using `build_feature_vector(assessment)`.
3. Instantiate `MLFeatureEncoder()` and call `load_preprocessor()`.
4. Call `encoder.transform(df)` to get the exact scaled feature array.
5. Pass the array to the trained model's `.predict()` method.

## Maintaining Feature Names
Categorical feature names expand after One-Hot-Encoding. The `MLFeatureEncoder` automatically dumps `feature_mapping.json` mapping original columns to their encoded variants, which is essential for libraries like SHAP or LIME to provide explainability.
