from typing import Dict, Any, List
from app.ai.copilot.providers.provider import LLMProvider
from app.ai.copilot.prompt_manager import PromptManager
from app.ai.copilot.recommendation_engine import RecommendationEngine
from app.ai.copilot.citation_service import CitationService
from app.ai.copilot.context_validator import ContextValidator
from app.ai.copilot.response_validator import ResponseValidator

class ReportGenerator:
    """
    Generates specialized security reports for different audiences (Executive, Engineer, Developer, Compliance).
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.prompt_manager = PromptManager()
        self.recommendation_engine = RecommendationEngine()
        self.citation_service = CitationService()
        
    def generate(self, audience: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a comprehensive report for the specified audience.
        Audience must be one of: 'executive', 'technical', 'developer', 'compliance'.
        """
        if not ContextValidator.validate(context):
            raise ValueError("Incomplete or missing ML Context. Cannot generate report.")
            
        valid_audiences = ["executive", "technical", "developer", "compliance"]
        if audience not in valid_audiences:
            audience = "executive"
            
        prompt = self.prompt_manager.get_prompt(audience)
        
        # Inject recommendations into the context before generation
        recs = self.recommendation_engine.generate_recommendations(context)
        context["generated_recommendations"] = self.citation_service.append_citations(recs)
        
        # Generate via Provider
        raw_report = self.provider.generate_report(context, prompt)
        
        # Validate LLM output
        if not ResponseValidator.validate(raw_report, context):
            # In a real app, we might retry or return a canned safe response
            raw_report += "\n\n[Warning: Potential deviation from ML findings detected in this generation.]"
            
        # Append Citations
        final_report = raw_report + self.citation_service.build_citation_footer(context)
        
        return {
            "audience": audience,
            "report_text": final_report,
            "recommendations": context["generated_recommendations"]
        }
