from typing import Dict, Any
from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from app.ml.trend_prediction.trend_schema import TrendSchema
from app.ai.copilot.providers.gemini_provider import GeminiProvider
from app.ai.copilot.context_builder import ContextBuilder
from app.ai.copilot.report_generator import ReportGenerator
from app.ai.copilot.conversation_service import ConversationService

class CopilotService:
    """
    Centralized entry point for all AI Copilot interactions.
    Abstracts away provider initialization and component wiring.
    """
    
    def __init__(self):
        # In an enterprise app, this might be injected via dependency injection 
        # or loaded based on environment variables (e.g. LLM_PROVIDER=gemini)
        self.provider = GeminiProvider()
        self.report_generator = ReportGenerator(self.provider)
        self.conversation_service = ConversationService(self.provider)
        
    def generate_dashboard_report(self, prediction: UnifiedPrediction, trend: TrendSchema = None, audience: str = "executive") -> Dict[str, Any]:
        """
        Generates the final report payload suitable for the frontend dashboard.
        """
        context = ContextBuilder.build_context(prediction, trend)
        report_data = self.report_generator.generate(audience, context)
        
        # Format payload for frontend API
        return {
            "audience": report_data["audience"],
            "summary": report_data["report_text"],
            "recommendations": report_data["recommendations"],
            "is_ai_generated": True,
            "provider": "Gemini (via Provider Abstraction)"
        }
        
    def handle_chat(self, session_id: str, prediction: UnifiedPrediction, trend: TrendSchema, user_message: str) -> str:
        """
        Processes an interactive chat message.
        """
        context = ContextBuilder.build_context(prediction, trend)
        return self.conversation_service.chat(session_id, context, user_message)
