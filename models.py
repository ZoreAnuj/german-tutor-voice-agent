"""
Data models for the German Language Practice Agent
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ConversationHistory:
    """Represents a single conversation exchange"""
    user_message: str
    tutor_response: str
    timestamp: str
    corrections: List[str] = None
    
    def __post_init__(self):
        if self.corrections is None:
            self.corrections = []


@dataclass
class TutorConfig:
    """Configuration for the German tutor"""
    model_name: str = "llama3.1:latest"
    ollama_url: str = "http://localhost:11434"
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 500
    voice_enabled: bool = True
    start_timeout: int = 10
    phrase_time_limit: int = 30
