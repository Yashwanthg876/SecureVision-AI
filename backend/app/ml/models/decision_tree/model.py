from sklearn.tree import DecisionTreeClassifier
from typing import Any, Dict

def create_decision_tree(**kwargs) -> DecisionTreeClassifier:
    """
    Factory function for Decision Tree model.
    """
    return DecisionTreeClassifier(**kwargs)
