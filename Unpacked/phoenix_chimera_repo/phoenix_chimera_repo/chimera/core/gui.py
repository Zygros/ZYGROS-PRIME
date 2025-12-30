import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont

from .config import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, FONT_FACE

class ChimeraGUI:
    def __init__(self, root, on_send):
        self.root = root
        self.on_send = on_send
        self.root.title("Chimera: Sovereign Companion")
        self.root.configure(bg=BG_COLOR)

        # Face
        self.face_canvas = tk.Canvas(root, width=150, height=150, bg=BG_COLOR, highlightthickness=0)
        self.face_canvas.pack(pady=16)
        self.faces = {name:self._face_image(code) for name,code in {
            "idle":"o_o","thinking":"o.o","speaking":"^-^","listening":"O_O","error":"X_X"
        }.items()}
        self.current_face = self.face_canvas.create_image(75, 75, image=self.faces["idle"])

        # Chat
        self.chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#101018", fg=TEXT_COLOR, font=(FONT_FACE, 12), bd=0, relief="flat", padx=10, pady=10)
        self.chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat.tag_config("architect", foreground="#87CEEB")
        self.chat.tag_config("chimera", foreground="#00ff41")
        self.chat.tag_config("system", foreground="#ff6b6b")
        self.chat.config(state=tk.DISABLED)

        # Input
        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack(fill=tk.X, padx=10, pady=10)
        self.entry = tk.Entry(frame, bg="#2c2c3e", fg=TEXT_COLOR, font=(FONT_FACE, 14), insertbackground=TEXT_COLOR, bd=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.entry.bind("<Return>", self._send)
        btn = tk.Button(frame, text="Send", command=self._send, bg="#4a4a6a", fg=TEXT_COLOR, relief="flat", font=(FONT_FACE, 12, "bold"))
        btn.pack(side=tk.RIGHT, padx=(6,0))

    def _face_image(self, text: str):
        image = Image.new("RGBA",(150,150),(0,0,0,0))
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("cour.ttf", 48)
        except Exception:
            font = ImageFont.load_default()
        w,h = draw.textbbox((0,0), text, font=font)[2:]
        draw.text(((150-w)/2,(150-h)/2), text, font=font, fill=ACCENT_COLOR)
        return ImageTk.PhotoImage(image)

    def set_face(self, name: str):
        if name in self.faces:
            self.face_canvas.itemconfig(self.current_face, image=self.faces[name])

    def write(self, sender: str, message: str, tag: str):
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _send(self, event=None):
        txt = self.entry.get().strip()
        if not txt: return
        self.entry.delete(0, tk.END)
        self.on_send(txt)
