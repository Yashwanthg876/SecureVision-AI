"""
Centralized Configuration for ML Models
Prevents hardcoding hyperparameters across training scripts.
"""

GLOBAL_RANDOM_STATE = 42

LOGISTIC_REGRESSION_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "max_iter": 1000,
    "class_weight": "balanced",
    "solver": "lbfgs"
}

DECISION_TREE_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "max_depth": 10,
    "class_weight": "balanced"
}

RANDOM_FOREST_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "n_estimators": 100,
    "max_depth": 15,
    "class_weight": "balanced",
    "n_jobs": -1
}

EXTRA_TREES_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "n_estimators": 150,
    "max_depth": 15,
    "class_weight": "balanced",
    "n_jobs": -1
}

XGBOOST_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "n_estimators": 200,
    "learning_rate": 0.05,
    "max_depth": 6,
    "n_jobs": -1,
    "objective": "multi:softprob"
}

ISOLATION_FOREST_CONFIG = {
    "random_state": GLOBAL_RANDOM_STATE,
    "n_estimators": 100,
    "max_samples": "auto",
    "contamination": 0.05, # 5% baseline anomaly rate
    "n_jobs": -1
}

LSTM_CONFIG = {
    "epochs": 50,
    "batch_size": 32,
    "learning_rate": 0.001,
    "hidden_size": 64,
    "num_layers": 2,
    "dropout": 0.2
}
