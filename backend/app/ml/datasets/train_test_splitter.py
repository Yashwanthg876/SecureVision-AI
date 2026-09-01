from typing import Tuple, Optional
import numpy as np
from sklearn.model_selection import train_test_split

def split_dataset(
    X: np.ndarray, 
    y: np.ndarray, 
    test_size: float = 0.2, 
    val_size: float = 0.0, 
    random_state: int = 42, 
    stratify: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Splits the dataset into Train, Test, and optionally Validation sets.
    Returns: X_train, X_test, y_train, y_test, X_val, y_val
    """
    stratify_labels = y if stratify else None
    
    # First split: Train vs Temp (Test + Val)
    temp_size = test_size + val_size
    if temp_size >= 1.0 or temp_size <= 0.0:
        raise ValueError("Combined test_size and val_size must be between 0 and 1.")
        
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, 
        test_size=temp_size, 
        random_state=random_state, 
        stratify=stratify_labels
    )
    
    if val_size == 0.0:
        return X_train, X_temp, y_train, y_temp, None, None
        
    # Second split: Test vs Val
    stratify_temp = y_temp if stratify else None
    val_ratio = val_size / temp_size
    
    X_test, X_val, y_test, y_val = train_test_split(
        X_temp, y_temp, 
        test_size=val_ratio, 
        random_state=random_state, 
        stratify=stratify_temp
    )
    
    return X_train, X_test, y_train, y_test, X_val, y_val
