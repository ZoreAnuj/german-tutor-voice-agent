# German Tutor Voice Agent

AI-powered German language tutor with voice recognition and real-time conversational practice using local LLMs.

## Overview

Interactive voice agent that listens to spoken German, processes it through a local LLM (Ollama), and responds with corrections and guidance via text-to-speech. Designed for immersive language practice through natural dialogue.

## Stack

| Component | Tech |
|-----------|------|
| Speech recognition | SpeechRecognition + PyAudio |
| LLM | Ollama (local inference) |
| TTS | pyttsx3 |
| Conversation | Custom prompt chain with tutor persona |

## Structure

```
main.py                  # Entry point, voice interaction loop
conversation_manager.py  # Dialogue state + history management
speech_handler.py        # Mic input + TTS output
ollama_client.py         # Local LLM API client
tutor_prompts.py         # System prompts for tutor behavior
models.py                # Data models
```

## Setup

```bash
pip install -r requirements.txt
# Requires Ollama running locally
python main.py
```
