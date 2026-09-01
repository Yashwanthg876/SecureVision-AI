import re
from typing import Dict, Tuple

class FeatureMapper:
    """
    Maps raw one-hot encoded or scaled features back to human-readable names and categories.
    """
    CATEGORY_MAPPING = {
        'ssl': 'SSL',
        'headers': 'Headers',
        'dns': 'DNS',
        'whois': 'WHOIS',
        'tech': 'Technology',
        'score': 'Scores'
    }

    @staticmethod
    def map_feature(raw_feature: str) -> Tuple[str, str]:
        """
        Takes a raw feature name (e.g., 'technology_details_server_nginx') 
        and returns a tuple of (Human Readable Name, Category).
        """
        # Determine category based on prefix
        category = "Configuration"
        for key, cat_name in FeatureMapper.CATEGORY_MAPPING.items():
            if key in raw_feature.lower():
                category = cat_name
                break
                
        # Simple cleanup rules
        readable = raw_feature.replace("_", " ").title()
        
        # Remove common one-hot encoding prefixes if they exist
        prefixes_to_strip = [
            "Technology Details Server", 
            "Technology Details Framework",
            "Headers Details",
            "Dns Details",
            "Ssl Details",
            "Whois Details"
        ]
        
        for prefix in prefixes_to_strip:
            if readable.startswith(prefix):
                # E.g., "Technology Details Server Nginx" -> "Server: Nginx"
                remainder = readable.replace(prefix, "").strip()
                if "Server" in prefix:
                    readable = f"Server: {remainder}"
                elif "Framework" in prefix:
                    readable = f"Framework: {remainder}"
                else:
                    readable = f"{category}: {remainder}"
                    
        # Score cleanups
        if "Score" in readable and category != "Scores":
            readable = readable.replace("Score", "").strip() + " Score"
            category = "Scores"

        return readable, category
