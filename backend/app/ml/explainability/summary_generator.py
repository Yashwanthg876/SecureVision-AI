from typing import List
from app.ml.explainability.explanation_schema import FeatureContribution

class SummaryGenerator:
    """
    Generates rule-based natural language summaries for explanations without relying on an LLM.
    """
    
    @staticmethod
    def generate_summary(
        prediction: str, 
        top_positive: List[FeatureContribution], 
        top_negative: List[FeatureContribution]
    ) -> str:
        
        if prediction in ["High", "Critical"]:
            if top_positive:
                factors = [f.feature for f in top_positive[:2]]
                factors_str = " and ".join(factors)
                return f"{factors_str} contributed most to the {prediction} Risk prediction."
            else:
                return f"The model determined a {prediction} Risk based on aggregated indicators."
                
        elif prediction in ["Low"]:
            if top_negative:
                factors = [f.feature for f in top_negative[:2]]
                factors_str = " and ".join(factors)
                return f"Strong security postures in {factors_str} heavily drove the {prediction} Risk prediction."
            else:
                return f"The model determined a {prediction} Risk based on general security compliance."
                
        else:
            # Medium
            pos = [f.feature for f in top_positive[:1]]
            neg = [f.feature for f in top_negative[:1]]
            if pos and neg:
                return f"A balance between risks ({pos[0]}) and strengths ({neg[0]}) resulted in a {prediction} Risk classification."
            elif pos:
                return f"Moderate risks identified in {pos[0]} led to the {prediction} Risk classification."
            else:
                return f"The assessment was classified as {prediction} Risk based on mixed indicators."
