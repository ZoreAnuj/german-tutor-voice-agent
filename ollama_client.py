"""
Ollama client for interacting with the German language model
"""

import requests
from typing import List, Dict


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, model_name: str = "llama3.1:latest", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and the model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                return self.model_name in model_names
            return False
        except requests.exceptions.RequestException:
            return False
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, 
                         top_p: float = 0.9, max_tokens: int = 500, timeout: int = 60) -> str:
        """Generate a response from the German tutor"""
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "Entschuldigung, ich konnte keine Antwort generieren.")
            else:
                return f"Fehler bei der Anfrage an Ollama: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Verbindungsfehler: {str(e)}"
        except Exception as e:
            return f"Unerwarteter Fehler: {str(e)}"
