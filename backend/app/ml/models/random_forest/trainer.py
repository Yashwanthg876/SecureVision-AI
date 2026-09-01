from sklearn.ensemble import RandomForestClassifier
from app.ml.models.ensemble.base_ensemble import BaseEnsembleTrainer

class RandomForestTrainer(BaseEnsembleTrainer):
    """
    Trainer for Random Forest Model.
    """
    def __init__(self, hyperparameters: dict, schema_version: str = "1.0"):
        super().__init__(
            model_name="Random Forest",
            model_factory=RandomForestClassifier,
            hyperparameters=hyperparameters,
            schema_version=schema_version
        )
