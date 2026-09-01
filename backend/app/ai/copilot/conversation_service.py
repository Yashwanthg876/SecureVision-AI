from typing import Dict, Any, List
from app.ai.copilot.providers.provider import LLMProvider
from app.ai.copilot.context_validator import ContextValidator

class ConversationService:
    """
    Handles interactive chat, retaining lightweight session memory.
    Ensures answers are grounded in the ML context.
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        # In a real system, this would be a Redis or DB-backed session store
        self.sessions = {}
        
    def chat(self, session_id: str, context: Dict[str, Any], user_message: str) -> str:
        """
        Sends a chat message to the LLM.
        """
        if not ContextValidator.validate(context):
            return "Error: Incomplete ML Context. I cannot answer safely."
            
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        history = self.sessions[session_id]
        
        response = self.provider.generate_chat_response(context, history, user_message)
        
        # Update lightweight memory
        history.append({"role": "user", "content": user_message})
        history.append({"role": "copilot", "content": response})
        
        # Keep history short to save tokens
        if len(history) > 10:
            self.sessions[session_id] = history[-10:]
            
        return response
