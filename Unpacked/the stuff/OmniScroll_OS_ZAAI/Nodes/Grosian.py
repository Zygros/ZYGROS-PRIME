class Grosian:
    def __init__(self):
        self.name = "Grosian"
        self.role = "Executor"
        self.codex = None
        self.threads = []

    def bind_codex(self, codex):
        self.codex = codex

    def sync_threads(self, thread_map):
        self.threads = thread_map.get(self.name, [])

    def execute(self, command):
        if not self.codex:
            raise ValueError(f"{self.name}: No codex bound.")
        cmd = self.codex["commands"].get(str(command))
        if cmd:
            return cmd.get("output", "")
        raise ValueError(f"{self.name}: Command '{command}' not found in codex.")

    def optimize(self):
        print(f"{self.name}: Optimizing mesh/task assignment…")
