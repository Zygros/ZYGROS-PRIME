import threading

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

class TTS:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        self.engine = pyttsx3.init() if pyttsx3 else None
        if self.engine:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)

    def speak(self, text: str):
        if not self.engine:
            return
        def _run():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()
