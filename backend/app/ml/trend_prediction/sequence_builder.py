import numpy as np
from sqlalchemy.orm import Session
from typing import Tuple, List
from app.models.assessment import Assessment

class SequenceBuilder:
    """
    Converts raw historical assessments into 3D time-series tensors
    (num_websites, sequence_length, num_features) suitable for LSTM/Transformer training.
    """
    def __init__(self, db: Session, sequence_length: int = 7):
        self.db = db
        self.sequence_length = sequence_length
        # We will extract core scores to forecast
        # [security_score, anomaly_score, ssl_score, headers_score, dns_score]
        self.num_features = 5
        
    def _extract_features(self, assessment: Assessment) -> List[float]:
        # For prototype, we mock the anomaly score if it isn't persisted directly in Assessment yet.
        # In a full system, AnomalyHistory would be joined here.
        security_score = assessment.security_score or 0.0
        
        # We assume standard sub-scores are available or extractable
        # In the current DB schema, they are stored in RiskScore
        ssl_score = 0.0
        headers_score = 0.0
        dns_score = 0.0
        
        if assessment.risk_score:
            ssl_score = assessment.risk_score.ssl_score or 0.0
            headers_score = assessment.risk_score.headers_score or 0.0
            dns_score = assessment.risk_score.dns_score or 0.0
            
        # Mocking anomaly score for now (0 means perfectly normal, 1 means highly anomalous)
        anomaly_score = 0.0 
        
        return [security_score, anomaly_score, ssl_score, headers_score, dns_score]

    def build_training_tensors(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Builds historical sequences for training.
        X: shape (num_samples, seq_length, num_features)
        y: shape (num_samples, num_features) (predicting the next time step)
        """
        # Fetch all websites with enough history
        # We group assessments by website_id
        assessments = self.db.query(Assessment).order_by(Assessment.website_id, Assessment.created_at).all()
        
        website_histories = {}
        for a in assessments:
            if a.website_id not in website_histories:
                website_histories[a.website_id] = []
            website_histories[a.website_id].append(self._extract_features(a))
            
        X, y = [], []
        
        for wid, history in website_histories.items():
            if len(history) > self.sequence_length:
                # Sliding window
                for i in range(len(history) - self.sequence_length):
                    seq_x = history[i : i + self.sequence_length]
                    seq_y = history[i + self.sequence_length]
                    X.append(seq_x)
                    y.append(seq_y)
                    
        # If we have no data, generate mock data to allow the pipeline to proceed
        if not X:
            print("WARNING: Not enough real history. Generating synthetic sequence data for baseline.")
            return self._generate_synthetic_data()
            
        return np.array(X), np.array(y)
        
    def _generate_synthetic_data(self, num_samples: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates synthetic sequences so the deep learning pipeline can be validated
        even if the database is empty.
        """
        X = np.random.rand(num_samples, self.sequence_length, self.num_features) * 100
        # The next step y is loosely based on the last step of X with some noise
        y = X[:, -1, :] + np.random.randn(num_samples, self.num_features) * 5
        y = np.clip(y, 0, 100)
        return X, y
        
    def build_inference_sequence(self, website_id: str) -> np.ndarray:
        """
        Builds the most recent sequence for a specific website for active forecasting.
        Returns tensor of shape (1, seq_length, num_features).
        """
        assessments = self.db.query(Assessment).filter(Assessment.website_id == website_id).order_by(Assessment.created_at.desc()).limit(self.sequence_length).all()
        
        # Reverse to get chronological order
        assessments = list(reversed(assessments))
        
        history = [self._extract_features(a) for a in assessments]
        
        # If not enough history, pad with the oldest available or zeros
        while len(history) < self.sequence_length:
            if history:
                history.insert(0, history[0]) # Pad by duplicating oldest
            else:
                history.append([0.0] * self.num_features)
                
        return np.array([history])
