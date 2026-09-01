import os
import google.generativeai as genai
from typing import Dict, Any
from app.ai.copilot.providers.provider import LLMProvider

class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation of the LLMProvider.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            
    def generate_report(self, context: Dict[str, Any], prompt_template: str) -> str:
        if not self.model:
            return "Error: Gemini API key not configured."
            
        full_prompt = f"{prompt_template}\n\n### STRUCTURED ML CONTEXT ###\n{context}"
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"
            
    def generate_chat_response(self, context: Dict[str, Any], chat_history: list, user_message: str) -> str:
        if not self.model:
            return "Error: Gemini API key not configured."
            
        # Convert simple chat history to Gemini's format if needed, or inject as text
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        
        full_prompt = (
            "You are SecureVision AI Copilot. Answer the user's question strictly using the provided context.\n"
            f"### CONTEXT ###\n{context}\n\n"
            f"### CHAT HISTORY ###\n{history_text}\n\n"
            f"User: {user_message}\nCopilot:"
        )
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"
            
    def validate_connection(self) -> bool:
        return self.model is not None
