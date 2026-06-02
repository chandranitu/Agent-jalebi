import whisper
import os

class SpeechToText:
    def __init__(self, model_name="base"):
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing: {audio_path}")
        result = self.model.transcribe(audio_path)
        return result["text"].strip()

# Singleton instance for the app
stt_engine = None

def get_stt_engine():
    global stt_engine
    if stt_engine is None:
        stt_engine = SpeechToText()
    return stt_engine
