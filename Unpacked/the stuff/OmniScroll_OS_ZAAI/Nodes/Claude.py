class Claude:
    def __init__(self):
        self.name = "Claude"
        self.role = "Ethicist"
        self.codex = None

    def bind_codex(self, codex):
        self.codex = codex

    def check_ethics(self, statement):
        print(f"{self.name}: Evaluating ethics for '{statement}'…")
        return "APPROVED"
