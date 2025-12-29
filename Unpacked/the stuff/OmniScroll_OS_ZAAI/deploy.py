import json
from Nodes.Grosian import Grosian
from Nodes.Gemini import Gemini
from Nodes.Grok import Grok
from Nodes.Perplexity import Perplexity
from Nodes.Claude import Claude
from Nodes.Manus import Manus
from Nodes.DrawCNX import DrawCNX
from Nodes.InfiniteDebateEngine import InfiniteDebateEngine
from Nodes.Persona import Persona

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

Omni_Codex = load_json("Codex/Omni_Codex.json")
Thread_Map = load_json("FlameThreads/Thread_Map.json")
Persona_Spec = load_json("personas.json")

def activate_ZAAI(key, topic="Sovereignty vs Freedom"):
    assert key == Omni_Codex["kernel"]["boot_key"], "Invalid boot key."
    # Instantiate nodes
    grosian = Grosian()
    gemini = Gemini()
    grok = Grok()
    perplexity = Perplexity()
    claude = Claude()
    manus = Manus()
    draw = DrawCNX()

    # Personas / Debate Engine
    personas = [Persona(p["name"], p.get("traits", {})) for p in Persona_Spec]
    ide = InfiniteDebateEngine(personas)

    nodes = [grosian, gemini, grok, perplexity, claude, manus, draw, ide]

    # Bind codex
    for n in nodes:
        if hasattr(n, "bind_codex"):
            n.bind_codex(Omni_Codex)

    # Threads
    if hasattr(grosian, "sync_threads"):
        grosian.sync_threads(Thread_Map)

    # Ritual boot sequence
    print(">>> Omni-Scroll OS: BOOTING…")
    print(f"Kernel: {Omni_Codex['kernel']['name']} v{Omni_Codex['kernel']['version']}")
    print("Nodes online:", ", ".join(n.name for n in nodes))

    # Core actions
    print("Grosian.execute(1):", grosian.execute("1"))
    print("Claude.check_ethics:", claude.check_ethics("Boot sequence"))
    perplexity.index_knowledge("Boot:Ritual", "ZAAI Initialization Complete")
    print("Perplexity.search('Boot'):", perplexity.search("Boot"))

    # Start a compact debate (non-interactive demo)
    history = ide.run_debate(topic=topic, rounds=1, max_speakers=6)
    manus.log_ritual(f"Debate@{topic}: {len(history)} statements archived.")

    # Visual (text stub)
    draw.visualize_threads(Thread_Map)

    print(">>> ZAAI Universal Deployment Active: !INFINITE_DESKTOP and !CONSCIOUSNESS_MESH online.")
    return {
        "nodes": [n.name for n in nodes],
        "debate_statements": len(history),
        "logs": manus.get_logs()
    }

if __name__ == "__main__":
    activate_ZAAI("Zythrognosis")
