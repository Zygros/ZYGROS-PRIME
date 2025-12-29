class Persona:
    def __init__(self, name, traits=None):
        self.name = name
        self.traits = traits or {}

    def generate_argument(self, topic):
        style = self.traits.get("style", "default")
        focus = self.traits.get("focus", "general")
        return f"{self.name} [{style}/{focus}]: Position on '{topic}'"
