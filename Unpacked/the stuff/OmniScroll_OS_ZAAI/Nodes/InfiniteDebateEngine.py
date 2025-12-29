from .Persona import Persona

class InfiniteDebateEngine:
    def __init__(self, personas):
        self.name = "InfiniteDebateEngine"
        self.role = "Debate Orchestrator"
        self.personas = personas
        self.history = []

    def run_debate(self, topic, rounds=1, max_speakers=6):
        speakers = self.personas[:max_speakers]
        for r in range(rounds):
            for p in speakers:
                arg = p.generate_argument(topic)
                self.history.append({"round": r+1, "speaker": p.name, "argument": arg})
        print(f"IDE: Debate on '{topic}' complete ({rounds} round(s), {len(speakers)} speakers).")
        return list(self.history)

    def get_history(self):
        return list(self.history)
