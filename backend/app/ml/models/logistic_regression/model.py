from sklearn.linear_model import LogisticRegression
from typing import Any, Dict

def create_logistic_regression(**kwargs) -> LogisticRegression:
    """
    Factory function for Logistic Regression model.
    """
    return LogisticRegression(**kwargs)
