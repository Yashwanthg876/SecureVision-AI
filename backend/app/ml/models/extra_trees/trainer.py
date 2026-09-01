from sklearn.ensemble import ExtraTreesClassifier
from app.ml.models.ensemble.base_ensemble import BaseEnsembleTrainer

class ExtraTreesTrainer(BaseEnsembleTrainer):
    """
    Trainer for Extra Trees Model.
    """
    def __init__(self, hyperparameters: dict, schema_version: str = "1.0"):
        super().__init__(
            model_name="Extra Trees",
            model_factory=ExtraTreesClassifier,
            hyperparameters=hyperparameters,
            schema_version=schema_version
        )
