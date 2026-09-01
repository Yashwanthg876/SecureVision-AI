import shap
from typing import Any

class ExplainerAdapter:
    """
    Automatically selects and initializes the correct SHAP Explainer 
    based on the model type.
    """
    
    @staticmethod
    def get_explainer(model: Any, background_data: Any = None):
        """
        Takes a loaded prediction model (from model_loader) and returns the optimal SHAP explainer.
        """
        # We need to inspect the inner Scikit-Learn/XGBoost model, not the GenericPredictionModel wrapper
        raw_model = model._model if hasattr(model, '_model') else model
        
        # If it's wrapped in a ProbabilityCalibrator or CalibratedClassifierCV
        if hasattr(raw_model, "calibrated_model"):
            raw_model = raw_model.calibrated_model
            
        if type(raw_model).__name__ == 'CalibratedClassifierCV':
            # SHAP can struggle with CalibratedClassifierCV out of the box for TreeExplainer
            # We attempt to extract the base estimator if it's fitted
            if hasattr(raw_model, "calibrated_estimators_") and len(raw_model.calibrated_estimators_) > 0:
                raw_model = raw_model.calibrated_estimators_[0].estimator
            elif hasattr(raw_model, "estimator"):
                raw_model = raw_model.estimator

        model_class_name = type(raw_model).__name__
        
        # Tree-based models (XGBoost, Random Forest, Extra Trees, Decision Tree)
        if model_class_name in ['XGBClassifier', 'RandomForestClassifier', 'ExtraTreesClassifier', 'DecisionTreeClassifier']:
            return shap.TreeExplainer(raw_model)
            
        # Linear models (Logistic Regression)
        elif model_class_name in ['LogisticRegression']:
            if background_data is None:
                raise ValueError("LinearExplainer requires background_data to compute SHAP values.")
            return shap.LinearExplainer(raw_model, background_data)
            
        # Fallback to KernelExplainer (Model agnostic but slow)
        else:
            if background_data is None:
                raise ValueError(f"KernelExplainer requires background_data for model type {model_class_name}.")
            # Using predict_proba if available, else predict
            predict_fn = raw_model.predict_proba if hasattr(raw_model, "predict_proba") else raw_model.predict
            # We use a summary of the background data for speed
            background_summary = shap.kmeans(background_data, 10) if len(background_data) > 10 else background_data
            return shap.KernelExplainer(predict_fn, background_summary)
