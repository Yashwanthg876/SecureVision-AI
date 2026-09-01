import os

class PromptManager:
    """
    Manages loading and versioning of markdown prompt templates.
    Ensures prompts are not hardcoded in Python.
    """
    def __init__(self):
        self.prompts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prompts'))
        
    def _create_default_if_missing(self, name: str, default_content: str):
        path = os.path.join(self.prompts_dir, f"{name}.md")
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(default_content)
                
    def get_prompt(self, audience: str) -> str:
        """
        Loads the specific prompt for the audience (e.g., executive, technical, developer, compliance)
        """
        # Create defaults if this is the first run
        self._create_default_if_missing("executive", 
            "You are SecureVision AI. Generate a concise, non-technical Executive Summary based on the provided ML risk context. Focus on business impact.")
        self._create_default_if_missing("technical", 
            "You are SecureVision AI. Generate a detailed Technical Report for a Security Engineer. Include SHAP explainability analysis and anomaly detection details.")
        self._create_default_if_missing("developer", 
            "You are SecureVision AI. Generate a Developer-focused remediation guide. Provide specific configuration fixes for the identified vulnerabilities.")
        self._create_default_if_missing("compliance", 
            "You are SecureVision AI. Generate a Compliance Report mapping the identified risks to frameworks like OWASP Top 10 or NIST.")
        self._create_default_if_missing("chat", 
            "You are SecureVision AI. Answer the user's question concisely based ONLY on the provided ML context.")
            
        path = os.path.join(self.prompts_dir, f"{audience}.md")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return "You are SecureVision AI. Analyze the context and provide a summary."
