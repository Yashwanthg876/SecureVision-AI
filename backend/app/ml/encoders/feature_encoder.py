import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

PREPROCESSING_DIR = os.path.join(os.path.dirname(__file__), '..', 'models', 'preprocessing')
PREPROCESSOR_PATH = os.path.join(PREPROCESSING_DIR, 'preprocessor.joblib')
FEATURE_MAPPING_PATH = os.path.join(PREPROCESSING_DIR, 'feature_mapping.json')

class MLFeatureEncoder:
    """
    Handles preprocessing and encoding of the raw FeatureVector vector 
    using scikit-learn and pandas to produce ML-ready NumPy arrays.
    Persists the pipeline for reproducibility.
    """
    def __init__(self):
        # We define the columns expected from our FeatureSchema
        self.numeric_features = [
            'cert_expiry_days', 'domain_age_days', 
            'ssl_score', 'headers_score', 'dns_score', 'tech_score'
        ]
        
        self.boolean_features = [
            'ssl_is_valid', 'has_hsts', 'has_csp', 'has_x_frame_options',
            'has_x_content_type_options', 'has_spf', 'has_dmarc'
        ]
        
        self.categorical_features = [
            'tls_version', 'server_software', 'framework'
        ]
        
        # Pipelines for each data type
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        boolean_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent'))
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Master preprocessor
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('bool', boolean_transformer, self.boolean_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])
            
        self.label_encoder = LabelEncoder()
        
    def fit_transform(self, df: pd.DataFrame, save_artifacts: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fits the encoders and transforms the dataset.
        Returns (X, y)
        """
        df_clean = df.copy()
        for col in self.boolean_features:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(float)
            
        X = self.preprocessor.fit_transform(df_clean)
        y = self.label_encoder.fit_transform(df_clean['label']) if 'label' in df_clean.columns else None
        
        if save_artifacts:
            self.save_preprocessor()
            self._generate_feature_mapping()
        
        return X, y
        
    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Transforms new data using previously fitted encoders.
        """
        df_clean = df.copy()
        for col in self.boolean_features:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(float)
            
        return self.preprocessor.transform(df_clean)
        
    def get_feature_names_out(self) -> List[str]:
        return list(self.preprocessor.get_feature_names_out())
        
    def save_preprocessor(self):
        os.makedirs(PREPROCESSING_DIR, exist_ok=True)
        joblib.dump({'preprocessor': self.preprocessor, 'label_encoder': self.label_encoder}, PREPROCESSOR_PATH)
        
    def load_preprocessor(self):
        if not os.path.exists(PREPROCESSOR_PATH):
            raise FileNotFoundError(f"Preprocessor not found at {PREPROCESSOR_PATH}")
        data = joblib.load(PREPROCESSOR_PATH)
        self.preprocessor = data['preprocessor']
        self.label_encoder = data['label_encoder']
        
    def _generate_feature_mapping(self):
        """
        Maintains a mapping between original feature names and encoded output features (e.g. for SHAP).
        """
        mapping = {
            "numeric": self.numeric_features,
            "boolean": self.boolean_features,
            "categorical_encoded": {}
        }
        
        # Extract OneHotEncoder output names
        try:
            ohe: OneHotEncoder = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
            ohe_features = ohe.get_feature_names_out(self.categorical_features)
            
            # Map them back to the original category
            for orig in self.categorical_features:
                mapping["categorical_encoded"][orig] = [f for f in ohe_features if f.startswith(orig + "_")]
        except Exception as e:
            print(f"Warning: Could not extract categorical feature mapping: {e}")
            
        mapping["all_output_features"] = self.get_feature_names_out()
        
        os.makedirs(PREPROCESSING_DIR, exist_ok=True)
        with open(FEATURE_MAPPING_PATH, 'w') as f:
            json.dump(mapping, f, indent=4)
