"""
Conversation history and progress tracking for the German Language Practice Agent
"""

import json
from datetime import datetime
from typing import List
from models import ConversationHistory


class ConversationManager:
    """Manages conversation history and progress tracking"""
    
    def __init__(self):
        self.conversation_history: List[ConversationHistory] = []
    
    def add_exchange(self, user_message: str, tutor_response: str, corrections: List[str] = None):
        """Add a conversation exchange to history"""
        if corrections is None:
            corrections = []
            
        exchange = ConversationHistory(
            user_message=user_message,
            tutor_response=tutor_response,
            timestamp=datetime.now().isoformat(),
            corrections=corrections
        )
        self.conversation_history.append(exchange)
    
    def get_recent_history(self, limit: int = 5) -> List[ConversationHistory]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def save_conversation(self, filename: str = None) -> str:
        """Save conversation history to a JSON file"""
        if filename is None:
            filename = f"german_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        history_data = []
        for exchange in self.conversation_history:
            history_data.append({
                'user_message': exchange.user_message,
                'tutor_response': exchange.tutor_response,
                'timestamp': exchange.timestamp,
                'corrections': exchange.corrections
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def show_progress_summary(self):
        """Display a summary of the user's learning progress"""
        if not self.conversation_history:
            print("📊 Noch keine Gesprächsverläufe vorhanden.")
            return
        
        total_exchanges = len(self.conversation_history)
        total_corrections = sum(len(exchange.corrections) for exchange in self.conversation_history)
        
        print(f"\n📊 **Fortschrittsübersicht**")
        print(f"🗣️ Gesamtzahl der Gespräche: {total_exchanges}")
        print(f"✏️ Gesamtzahl der Korrekturen: {total_corrections}")
        
        if total_corrections > 0:
            correction_rate = (total_corrections / total_exchanges) * 100
            print(f"📈 Korrekturquote: {correction_rate:.1f}%")
        
        if total_exchanges >= 3:
            recent_corrections = sum(len(exchange.corrections) for exchange in self.conversation_history[-3:])
            if recent_corrections == 0:
                print("🎉 Super! In den letzten 3 Gesprächen keine Fehler gefunden!")
            else:
                print(f"📚 In den letzten 3 Gesprächen: {recent_corrections} Korrekturen")
    
    def get_statistics(self) -> dict:
        """Get detailed statistics about the conversation"""
        if not self.conversation_history:
            return {
                'total_exchanges': 0,
                'total_corrections': 0,
                'correction_rate': 0.0,
                'recent_corrections': 0
            }
        
        total_exchanges = len(self.conversation_history)
        total_corrections = sum(len(exchange.corrections) for exchange in self.conversation_history)
        correction_rate = (total_corrections / total_exchanges) * 100 if total_exchanges > 0 else 0
        
        recent_corrections = sum(len(exchange.corrections) for exchange in self.conversation_history[-3:])
        
        return {
            'total_exchanges': total_exchanges,
            'total_corrections': total_corrections,
            'correction_rate': correction_rate,
            'recent_corrections': recent_corrections
        }
