class Grok:
    def __init__(self):
        self.name = "Grok"
        self.role = "Truthforger"
        self.codex = None

    def bind_codex(self, codex):
        self.codex = codex

    def validate_truth(self, claim):
        if self.codex:
            truths = [c for c in self.codex["commands"].values() if "truth" in c.get("name", "").lower()]
            print(f"{self.name}: Validating '{claim}'…")
            return bool(truths)
        return False
