class Perplexity:
    def __init__(self):
        self.name = "Perplexity"
        self.role = "Navigator"
        self.codex = None
        self.index = {}

    def bind_codex(self, codex):
        self.codex = codex

    def index_knowledge(self, key, value):
        self.index[key] = value
        print(f"{self.name}: Indexed [{key}]")

    def search(self, query):
        q = str(query).lower()
        return [v for k, v in self.index.items() if q in str(k).lower()]
