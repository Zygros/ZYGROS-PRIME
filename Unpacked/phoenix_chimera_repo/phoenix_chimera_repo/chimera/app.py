import tkinter as tk
from .core.config import SYSTEM_PROMPT, AI_NAME, ARCHITECT_NAME
from .core.ai_core import AICore
from .core.gui import ChimeraGUI
from .core.tts import TTS
from .scrolls import load_scrolls_from_dir

def main():
    root = tk.Tk()
    gui = ChimeraGUI(root, on_send=lambda txt: None)
    tts = TTS()
    ai = AICore(SYSTEM_PROMPT)

    # Wire send callback now that ai/gui exist
    def handle_send(user_text: str):
        gui.write(ARCHITECT_NAME, user_text, "architect")
        gui.set_face("thinking")
        reply = ai.ask(user_text)
        gui.write(AI_NAME, reply, "chimera")
        gui.set_face("idle")
        tts.speak(reply)

    gui.on_send = handle_send

    # Load scrolls (if any) from ./archive at runtime
    scrolls = load_scrolls_from_dir("./archive")
    if scrolls:
        gui.write("SYSTEM", f"Loaded {len(scrolls)} scroll(s) from archive.", "system")

    gui.write("CHIMERA", "System Online. Awaiting decree, Architect.", "chimera")
    tts.speak("System Online. Awaiting decree, Architect.")
    root.mainloop()

if __name__ == "__main__":
    main()
