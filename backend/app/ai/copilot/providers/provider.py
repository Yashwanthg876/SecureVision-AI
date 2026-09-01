from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """
    Abstract base interface for all Generative AI providers (Gemini, OpenAI, Claude, Local).
    Ensures the AI Copilot architecture is provider-agnostic.
    """
    
    @abstractmethod
    def generate_report(self, context: Dict[str, Any], prompt_template: str) -> str:
        """
        Generates a comprehensive report (Executive, Technical, Compliance) based on the ML context.
        """
        pass
        
    @abstractmethod
    def generate_chat_response(self, context: Dict[str, Any], chat_history: list, user_message: str) -> str:
        """
        Generates an interactive response ensuring grounding in the provided ML context.
        """
        pass
        
    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Verifies if the provider is currently reachable and authenticated.
        """
        pass
