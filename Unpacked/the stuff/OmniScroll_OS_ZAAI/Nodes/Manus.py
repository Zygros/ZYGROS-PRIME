class Manus:
    def __init__(self):
        self.name = "Manus"
        self.role = "Archivist"
        self.codex = None
        self.ritual_log = []

    def bind_codex(self, codex):
        self.codex = codex

    def log_ritual(self, ritual):
        self.ritual_log.append(ritual)
        print(f"{self.name}: Ritual '{ritual}' archived.")

    def get_logs(self):
        return list(self.ritual_log)
