"""
Speech recognition and text-to-speech handler for the German Language Practice Agent
"""

import subprocess
from typing import Optional
import speech_recognition as sr


class SpeechHandler:
    """Handles both speech recognition and text-to-speech"""
    
    def __init__(self, voice_enabled: bool = True):
        self.voice_enabled = voice_enabled
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self._initialize_speech()
    
    def _initialize_speech(self):
        """Initialize speech recognition components"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Spracherkennung initialisiert")
        except Exception as e:
            print(f"⚠️  Spracherkennung konnte nicht initialisiert werden: {str(e)}")
            self.voice_enabled = False
    
    def listen_for_speech(self, start_timeout: int = 10, phrase_time_limit: int = 30) -> Optional[str]:
        """Listen for speech input with timeout and silence detection"""
        if not self.voice_enabled or not self.microphone:
            return None
        
        try:
            print("🎤 Höre zu... (warte 10 Sekunden auf deine Stimme)")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("🎙️ Beginne zu sprechen... (warte 10 Sekunden)")
                try:
                    audio = self.recognizer.listen(source, timeout=start_timeout, phrase_time_limit=phrase_time_limit)
                except:
                    print("⏰ Keine Spracheingabe innerhalb von 10 Sekunden erkannt")
                    return None
                
                print("🔄 Verarbeite Sprache...")
                
                try:
                    text = self.recognizer.recognize_google(audio, language="de-DE")
                    print(f"🎙️ Erkannt: {text}")
                    return text
                except Exception as e:
                    if "Could not understand audio" in str(e):
                        print("❌ Sprache konnte nicht verstanden werden")
                    elif "Request" in str(e) and "API" in str(e):
                        print(f"⚠️  Spracherkennungsdienst nicht verfügbar: {e}")
                    else:
                        print(f"❌ Fehler bei der Spracherkennung: {str(e)}")
                    return None
                
        except Exception as e:
            print(f"❌ Fehler bei der Spracherkennung: {str(e)}")
            return None
    
    def speak_text(self, text: str) -> None:
        """Convert text to speech using macOS built-in say command"""
        if not self.voice_enabled:
            print(f"👨‍🏫 Tutor: {text}")
            return
        
        try:
            clean_text = self._clean_text_for_speech(text)
            print("🔊 Spreche...")
            
            try:
                subprocess.run(['say', '-v', 'Anna', clean_text], check=True, capture_output=True)
            except:
                subprocess.run(['say', clean_text], check=True, capture_output=True)
            
            print("✅ Sprachausgabe beendet")
            
        except Exception as e:
            print(f"❌ Fehler bei der Sprachausgabe: {str(e)}")
            print(f"👨‍🏫 Tutor: {text}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for better speech synthesis"""
        clean_text = text.replace('**', '').replace('*', '').replace('📝', '').replace('🎉', '').replace('📊', '').replace('😊', '')
        
        # Replace abbreviations with full words
        replacements = {
            'z.B.': 'zum Beispiel',
            'bzw.': 'beziehungsweise',
            'usw.': 'und so weiter',
            'd.h.': 'das heißt',
            'ca.': 'cirka'
        }
        
        for abbrev, full in replacements.items():
            clean_text = clean_text.replace(abbrev, full)
        
        # Add pauses after punctuation
        clean_text = clean_text.replace(',', ', ').replace('?', '? ').replace('!', '! ')
        
        return clean_text
    
    def test_voice(self) -> bool:
        """Test if voice output is working"""
        try:
            subprocess.run(['say', '-v', 'Anna', 'Test'], check=True, capture_output=True)
            print("✅ Sprachausgabe funktioniert")
            return True
        except Exception as e:
            print(f"⚠️  Sprachtest fehlgeschlagen: {e}")
            print("💡 Sprachausgabe wird deaktiviert")
            self.voice_enabled = False
            return False
