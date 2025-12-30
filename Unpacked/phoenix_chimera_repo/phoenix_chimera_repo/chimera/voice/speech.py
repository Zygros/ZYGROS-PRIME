# Optional speech input mapping: "voice is code"
# Requires microphone + SpeechRecognition (and possibly PyAudio).

import threading
try:
    import speech_recognition as sr
except Exception:
    sr = None

class SpeechCapture:
    def __init__(self, on_text):
        self.on_text = on_text
        self.running = False

    def start(self):
        if not sr: return
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as mic:
            while self.running:
                audio = r.listen(mic, phrase_time_limit=6)
                try:
                    txt = r.recognize_google(audio)
                    if txt:
                        self.on_text(txt)
                except Exception:
                    pass
