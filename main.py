#!/usr/bin/env python3
"""
German Language Practice Agent - Main Application
A conversational AI tutor for practicing German using Ollama and voice interaction
"""

import sys
import time
from models import TutorConfig
from speech_handler import SpeechHandler
from ollama_client import OllamaClient
from tutor_prompts import TutorPrompts
from conversation_manager import ConversationManager


class GermanTutor:
    """Main German tutor application"""
    
    def __init__(self, config: TutorConfig = None):
        self.config = config or TutorConfig()
        self.speech_handler = SpeechHandler(self.config.voice_enabled)
        self.ollama_client = OllamaClient(self.config.model_name, self.config.ollama_url)
        self.conversation_manager = ConversationManager()
        self.prompts = TutorPrompts()
        self.system_prompt = self.prompts.get_system_prompt()
        
        # Test voice if enabled
        if self.config.voice_enabled:
            self.speech_handler.test_voice()
    
    def generate_response(self, user_message: str) -> str:
        """Generate a response from the German tutor"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add recent conversation history
        recent_history = self.conversation_manager.get_recent_history(5)
        for exchange in recent_history:
            messages.append({"role": "user", "content": exchange.user_message})
            messages.append({"role": "assistant", "content": exchange.tutor_response})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        return self.ollama_client.generate_response(
            messages,
            self.config.temperature,
            self.config.top_p,
            self.config.max_tokens
        )
    
    def run_interactive_mode(self):
        """Run the interactive conversation mode with voice support"""
        print("🇩🇪 Willkommen bei deinem deutschen Sprachtutor!")
        print("📝 Ich bin hier, um dir beim Deutschlernen zu helfen.")
        
        if self.config.voice_enabled:
            print("🎤 Sprachmodus ist aktiviert - sprich einfach auf Deutsch!")
            print("⌨️  Tippe 'text' um auf Textmodus zu wechseln")
        else:
            print("⌨️  Textmodus - sprachfunktionen nicht verfügbar")
        
        print("🚀 Tippe 'beenden' zum Aufhören, 'fortschritt' für deine Statistik, oder 'speichern' zum Speichern des Gesprächs.\n")
        
        use_voice = self.config.voice_enabled
        
        while True:
            try:
                user_input = None
                
                if use_voice:
                    user_input = self.speech_handler.listen_for_speech(
                        self.config.start_timeout, 
                        self.config.phrase_time_limit
                    )
                    
                    if user_input is None:
                        print("⌨️  Bitte tippe deine Nachricht:")
                        user_input = input("👤 Du: ").strip()
                else:
                    user_input = input("👤 Du: ").strip()
                
                # Handle commands
                if user_input.lower() in ['beenden', 'exit', 'quit', 'aufhören']:
                    print("\n👋 Auf Wiedersehen! Weiter viel Erfolg beim Deutschlernen!")
                    break
                
                if user_input.lower() in ['fortschritt', 'progress']:
                    self.conversation_manager.show_progress_summary()
                    continue
                
                if user_input.lower() in ['speichern', 'save']:
                    filename = self.conversation_manager.save_conversation()
                    print(f"💬 Gespräch wurde in '{filename}' gespeichert")
                    continue
                
                if user_input.lower() in ['text']:
                    use_voice = False
                    print("⌨️  Gewechselt zu Textmodus")
                    continue
                
                if user_input.lower() in ['stimme', 'voice']:
                    if self.config.voice_enabled:
                        use_voice = True
                        print("🎤 Gewechselt zu Sprachmodus")
                    else:
                        print("❌ Sprachfunktionen nicht verfügbar")
                    continue
                
                if not user_input:
                    print("💡 Bitte sag mir etwas auf Deutsch...")
                    continue
                
                print("🤖 Denk nach...")
                response = self.generate_response(user_input)
                print(f"\n👨‍🏫 Tutor: {response}\n")
                
                # Speak the response if voice is enabled
                if use_voice:
                    self.speech_handler.speak_text(response)
                    time.sleep(1)  # Brief pause after speaking
                
                # Add to conversation history
                corrections = self.prompts.extract_corrections(response)
                self.conversation_manager.add_exchange(user_input, response, corrections)
                
            except KeyboardInterrupt:
                print("\n\n👋 Gespräch beendet. Bis zum nächsten Mal!")
                break
            except Exception as e:
                print(f"\n❌ Fehler: {str(e)}")
                continue


def main():
    """Main function to run the German tutor"""
    print("🇩🇪 German Language Practice Agent wird gestartet...")
    
    # Initialize tutor
    config = TutorConfig()
    tutor = GermanTutor(config)
    
    # Check Ollama connection
    print("🔍 Prüfe Ollama-Verbindung...")
    if not tutor.ollama_client.check_connection():
        print(f"❌ Fehler: Ollama läuft nicht oder das Modell '{config.model_name}' ist nicht verfügbar.")
        print("💡 Bitte stelle sicher, dass:")
        print("   1. Ollama installiert und läuft: https://ollama.ai")
        print(f"   2. Das Modell '{config.model_name}' heruntergeladen wurde:")
        print(f"      ollama pull {config.model_name}")
        sys.exit(1)
    
    print("✅ Ollama-Verbindung erfolgreich!")
    tutor.run_interactive_mode()


if __name__ == "__main__":
    main()
