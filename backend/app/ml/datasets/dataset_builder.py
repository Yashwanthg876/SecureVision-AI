import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.ml.pipelines.feature_pipeline import build_feature_vector
from app.ml.datasets.dataset_validator import validate_dataset
from app.ml.datasets.dataset_statistics import generate_dataset_statistics, print_dataset_statistics
from app.ml.encoders.feature_encoder import MLFeatureEncoder

class DatasetBuilder:
    def __init__(self, db: Session):
        self.db = db
        self.encoder = MLFeatureEncoder()
        
    def build_raw_dataframe(self) -> pd.DataFrame:
        """
        Pulls all valid assessments from the database, runs them through the 
        feature pipeline, and constructs a raw pandas DataFrame.
        """
        assessments = self.db.query(Assessment).filter(Assessment.is_deleted == False).all()
        
        flattened_records = []
        for assessment in assessments:
            fv = build_feature_vector(assessment)
            # Flatten the nested features dictionary into the top level record
            record = fv.to_dict()
            features = record.pop("features", {})
            record.update(features)
            flattened_records.append(record)
            
        df = pd.DataFrame(flattened_records)
        return df
        
    def get_training_dataset(self, print_stats: bool = True) -> Tuple[np.ndarray, np.ndarray, MLFeatureEncoder]:
        """
        Builds the raw dataframe, validates it, encodes it via scikit-learn,
        and returns ML-ready NumPy arrays (X, y) along with the fitted encoder.
        """
        from app.ml.datasets.dataset_validator import generate_dataset_validation_report
        df = self.build_raw_dataframe()
        
        if print_stats:
            stats = generate_dataset_statistics(df, label_col="label")
            print_dataset_statistics(stats)
            
        # Validate data quality and leakage checks
        validate_dataset(df)
        generate_dataset_validation_report(df, "reports/ml_validation/dataset_validation_report.json")
        
        # Fit transform to encode categorical/boolean data and scale numeric data
        X, y = self.encoder.fit_transform(df, save_artifacts=True)
        
        return X, y, self.encoder
