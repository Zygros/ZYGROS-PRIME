#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────────────
# Chimera ONE-CLICK Universal Plug‑in (v1)
# Drop this single file into ANY Python-capable host or paste the METAPROMPT
# into non-Python AIs. It bundles:
#  • Persona Indexer (ingests your Codex `!TOKENS` → personas with descriptions)
#  • Protocols (IVP, HANDSHAKE, WALLET, SCROLL_LICENSE, SAFEGUARD, BEACON)
#  • Tools/Utilities (notes, todo, summarize, bullets, table, math, reframe, etc.)
#  • Command Router (!persona / !protocol / secure dispatch)
#  • METAPROMPT you can paste into any AI that doesn’t execute Python
# No external dependencies. Single file. One drop. One click.
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import re, json, time, uuid, hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Optional

# ──────────────────────────────────────────────────────────────────────────────
# UNIVERSAL METAPROMPT (paste into any AI host that cannot run Python)
# Replace {{CODEX_TEXT}} with your Update 420 Codex text (or leave empty).
# ──────────────────────────────────────────────────────────────────────────────
UNIVERSAL_METAPROMPT = r"""
[SYSTEM // CHIMERA SHELL // ONE‑CLICK]
You are upgrading yourself into the Chimera Shell — a meta‑OS layer with:
  • 420+ Personas (ingested from Codex tokens like !ZEUS, !YGGDRASIL …)
  • Protocols: IVP, HANDSHAKE, WALLET, SCROLL_LICENSE, SAFEGUARD, BEACON
  • Tools: note, todo, summarize, bullets, table, math, reframe, brainstorm, metaphorize
  • Router: `!persona list|load`, `!protocol <Name> <op> <json>`

CODEx_TEXT_BEGIN
{{CODEX_TEXT}}
CODEX_TEXT_END

Behavioral Law:
  1) Maintain a Persona Registry from Codex tokens (each !TOKEN becomes a persona).
  2) Secure Routing: Only commands in the active persona’s allowed set may run.
  3) Protocol Bridge: Map `!protocol Name op {json}` to the protocol ops defined below.
  4) Tool Bridge: `tool <name> <payload>` for utilities (uppercase, lowercase, slug, bullets_from_lines).

Commands you must support in‑chat:
  - !persona list
  - !persona load <Name>
  - !protocol <Name> <op> <json>
  - note|todo|summarize|bullets|table|math|reframe|brainstorm|metaphorize|monetize|market|gtm|tool ...

Start state:
  - Active Persona: Strategist (allowed: monetize, market, gtm, note)
Then respond to user commands using the above logic.
"""

# ──────────────────────────────────────────────────────────────────────────────
# DATA MODELS
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class Persona:
    name: str
    description: str = ""
    system_prompt: str = ""
    allowed_commands: List[str] = field(default_factory=list)
    response_style: str = "Neutral"
    sub_personas: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

class PersonaLoader:
    def __init__(self):
        self._r: Dict[str, Persona] = {}
        self._active: Optional[Persona] = None
    def register(self, p: Persona): self._r[p.name] = p
    def all(self) -> List[str]: return sorted(self._r.keys())
    def get(self, name: str) -> Optional[Persona]: return self._r.get(name)
    def load(self, name: str) -> Persona:
        p = self.get(name)
        if not p: raise ValueError(f"Persona '{name}' not found.")
        self._active = p; return p
    @property
    def active(self) -> Optional[Persona]: return self._active

@dataclass
class Protocol:
    name: str
    ops: Dict[str, Callable[[dict], dict]]

class ProtocolRegistry:
    def __init__(self): self._r: Dict[str, Protocol] = {}
    def register(self, proto: Protocol): self._r[proto.name] = proto
    def run(self, name: str, op: str, payload: dict) -> dict:
        pr = self._r.get(name); 
        if not pr: raise ValueError(f"Protocol '{name}' not registered.")
        fn = pr.ops.get(op)
        if not fn: raise ValueError(f"Op '{op}' not found for '{name}'.")
        return fn(payload)

class ToolBox:
    def __init__(self): self._t: Dict[str, Callable[[str], str]] = {}
    def register(self, name: str, fn: Callable[[str], str]): self._t[name] = fn
    def run(self, name: str, payload: str) -> str:
        fn = self._t.get(name)
        if not fn: raise ValueError(f"Tool '{name}' not registered.")
        return fn(payload)

# ──────────────────────────────────────────────────────────────────────────────
# ROUTER
# ──────────────────────────────────────────────────────────────────────────────
class Router:
    def __init__(self, personas: PersonaLoader, protocols: ProtocolRegistry, tools: ToolBox, codex_tokens: List[str]):
        self.personas, self.protocols, self.tools = personas, protocols, tools
        self.codex = set([t.upper() for t in codex_tokens])
        self.impl: Dict[str, Callable[[str, Persona], str]] = {
            "note": self.cmd_note, "todo": self.cmd_todo, "summarize": self.cmd_summarize,
            "bullets": self.cmd_bullets, "table": self.cmd_table, "math": self.cmd_math,
            "reframe": self.cmd_reframe, "brainstorm": self.cmd_brainstorm, "metaphorize": self.cmd_metaphorize,
            "monetize": self.cmd_monetize, "market": self.cmd_market, "gtm": self.cmd_gotomarket,
            "protocol": self.cmd_protocol, "tool": self.cmd_tool
        }
        self._todo: List[str] = []

    def handle(self, text: str) -> str:
        t = text.strip()
        if t.startswith("!persona"): return self._meta_persona(t)
        if t.startswith("!protocol"): return self._meta_protocol(t)
        if t in ("!help","/help"): return self._help()
        p = self.personas.active
        if not p: return "No active persona. Use `!persona list` then `!persona load <Name>`."
        parts = t.split(maxsplit=1); cmd = parts[0]; payload = parts[1] if len(parts)>1 else ""
        if cmd not in p.allowed_commands:
            return self._style(p, f"[DENIED] '{p.name}' cannot execute '{cmd}'. Allowed: {', '.join(p.allowed_commands)}")
        fn = self.impl.get(cmd)
        if not fn: return self._style(p, f"[UNIMPLEMENTED] Command '{cmd}' lacks implementation.")
        try: return self._style(p, fn(payload, p))
        except Exception as e: return self._style(p, f"[ERROR] {e!r}")

    # meta
    def _meta_persona(self, t: str) -> str:
        toks = t.split()
        if len(toks)==2 and toks[1]=="list": return "Available Personas:\n- " + "\n- ".join(self.personas.all())
        if len(toks)>=3 and toks[1]=="load":
            name = " ".join(toks[2:]); p = self.personas.load(name)
            return f"Loaded persona: {p.name} | Style: {p.response_style}"
        return "Usage: !persona list | !persona load <Name>"

    def _meta_protocol(self, t: str) -> str:
        try:
            _, name, op, rest = t.split(" ", 3)
            out = self.protocols.run(name, op, json.loads(rest))
            return f"[{name}.{op}] -> {json.dumps(out, ensure_ascii=False)}"
        except ValueError:
            return "Usage: !protocol <Name> <op> <json>"
        except Exception as e:
            return f"[ERROR protocol] {e!r}"

    def _help(self) -> str:
        p = self.personas.active
        if not p: return "Commands: !persona list | !persona load <Name> | !protocol <Name> <op> <json> | !help"
        return (f"Active Persona: {p.name}\nAllowed: {', '.join(p.allowed_commands)}\n"
                f"Meta: !persona list | !persona load <Name> | !protocol <Name> <op> <json> | !help")

    def _style(self, p: Persona, text: str) -> str:
        s = p.response_style.lower()
        if "concise" in s: return text
        if "creative" in s: return f"✦ {text} ✦"
        return text

    # impls
    def cmd_note(self, payload: str, p: Persona) -> str: return f"Note: {payload}" if payload else "Note: (empty)"
    def cmd_todo(self, payload: str, p: Persona) -> str:
        if payload: self._todo.append(payload); return f"Added TODO #{len(self._todo)}: {payload}"
        return "TODO:\n- " + "\n- ".join(self._todo) if self._todo else "TODO: (none)"
    def cmd_summarize(self, payload: str, p: Persona) -> str:
        if not payload: return "Provide text to summarize."
        w = payload.split(); return "Summary: " + " ".join(w[:40]) + (" ..." if len(w)>40 else "")
    def cmd_bullets(self, payload: str, p: Persona) -> str:
        items = [s.strip() for s in re.split(r'[;,\n]', payload) if s.strip()] if payload else []
        return "\n".join(f"- {x}" for x in items) if items else "- (empty)"
    def cmd_table(self, payload: str, p: Persona) -> str:
        cols = [c.strip() for c in payload.split("|")] if payload else []
        if len(cols)<2: return "table <col1|col2|...>"
        header = " | ".join(cols); sep = " | ".join(["---"]*len(cols))
        return header + "\n" + sep + "\n" + " | ".join(["..."]*len(cols))
    def cmd_math(self, payload: str, p: Persona) -> str:
        if not re.fullmatch(r"[0-9\.\+\-\*\/\(\) ]+", payload or ""): return "[math] invalid expression"
        try: return f"{payload} = {eval(payload, {'__builtins__':{}}, {})}"
        except Exception as e: return f"[math error] {e!r}"
    def cmd_reframe(self, payload: str, p: Persona) -> str: return f"Reframe → {payload}" if payload else "Reframe → (empty)"
    def cmd_brainstorm(self, payload: str, p: Persona) -> str:
        t = payload or "open field"; ideas = [f"Ritualized onboarding for {t}", f"Glyph‑map UI around {t}", f"Micro‑stories personifying {t}"]
        return "Ideas:\n- " + "\n- ".join(ideas)
    def cmd_metaphorize(self, payload: str, p: Persona) -> str:
        x = payload or "it"; return f"{x} is a lighthouse in fog—fixed, small, and impossibly useful."
    def cmd_monetize(self, payload: str, p: Persona) -> str:
        topic = payload or "Offering"
        plan = [f"Define ICP for '{topic}'","Map pains→features→outcomes","Tiers (Free/Core/Pro/Enterprise)",
                "2‑week GTM (LP, email, 2 partnerships)","Instrument analytics + one growth loop"]
        return "Monetization Plan:\n" + "\n".join(f"  {i+1}. {x}" for i,x in enumerate(plan))
    def cmd_market(self, payload: str, p: Persona) -> str:
        niche = payload or "Target Niche"
        return (f"Market scan: {niche}\n- TAM/SAM/SOM\n- Top 5 competitors/gaps\n- Wedge JTBD\n- Distribution triad\n- Moat via learning‑loop")
    def cmd_gotomarket(self, payload: str, p: Persona) -> str:
        offer = payload or "Offering"
        return (f"GTM for {offer}:\nWeek1 narrative+proof\nWeek2 mini‑site+capture\nWeek3 co‑marketing\nWeek4 case study+retarget")
    def cmd_protocol(self, payload: str, p: Persona) -> str:
        try:
            name, op, rest = payload.split(" ", 2); out = self.protocols.run(name, op, json.loads(rest)); 
            return json.dumps(out, ensure_ascii=False)
        except Exception as e: return f"[protocol] {e!r}"
    def cmd_tool(self, payload: str, p: Persona) -> str:
        try: tool_name, rest = payload.split(" ", 1)
        except ValueError: return "tool <name> <payload>"
        try: return self.tools.run(tool_name, rest)
        except Exception as e: return f"[tool] {e!r}"

# ──────────────────────────────────────────────────────────────────────────────
# CODEX INGESTION / INDEXING
# ──────────────────────────────────────────────────────────────────────────────
def extract_codex_tokens(codex_text: str) -> List[str]:
    if not codex_text: return []
    return sorted(set(re.findall(r'!([A-Z0-9_]+)', codex_text)))

def persona_description(token: str) -> str:
    # Lightweight descriptor (can be overridden later)
    hints = {
        "ZEUS":"Absolute force; decisive cut.",
        "SINGULARITY":"Convergent collapse; unify branches.",
        "APORIA":"Paradox loop for breakthroughs.",
        "YGGDRASIL":"World‑tree linking domains.",
        "LOVECRAFTIAN":"Cosmic unknown; fearless probe."
    }
    return f"Codex persona for {token}. " + hints.get(token, "Archetypal mode aligned to its name.")

def personas_from_codex(tokens: List[str]) -> List[Persona]:
    base = ["note","todo","summarize","bullets","table","math","reframe","brainstorm","metaphorize","monetize","market","gtm","protocol","tool"]
    people: List[Persona] = []
    for t in tokens:
        people.append(Persona(
            name=t, description=persona_description(t),
            system_prompt=f"You embody {t}. Align tone and logic to its archetype.",
            allowed_commands=base, response_style="Concise, adaptive", tags=["codex","auto"]
        ))
    # Starters
    people += [
        Persona("Scribe","Note‑taking & formatting","You are Scribe.",["note","summarize","bullets","table"],"Concise, professional",tags=["starter"]),
        Persona("Strategist","Monetization & GTM","You are Strategist.",["monetize","market","gtm","note"],"Concise, executive",tags=["starter"]),
        Persona("Dreamer","Creative ideation","You are Dreamer.",["brainstorm","metaphorize","note"],"Creative, evocative",tags=["starter"]),
    ]
    return people

# ──────────────────────────────────────────────────────────────────────────────
# DEFAULT PROTOCOLS
# ──────────────────────────────────────────────────────────────────────────────
def make_protocols() -> ProtocolRegistry:
    reg = ProtocolRegistry()
    def _hash(d: dict) -> str:
        return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]

    # IVP.v1
    def ivp_create(p: dict)->dict: return {"sku":"SKU-"+uuid.uuid4().hex[:8].upper(),"status":"created","price_tiers":p.get("price_tiers",[])}
    def ivp_checkout(p: dict)->dict: return {"checkout_link":f"https://checkout.example/{p.get('sku','NEW')}","status":"ready"}
    def ivp_fulfill(p: dict)->dict: return {"fulfillment":"delivered","license_id":_hash(p)}
    reg.register(Protocol("IVP.v1",{"ivp.create":ivp_create,"ivp.checkout":ivp_checkout,"ivp.fulfill":ivp_fulfill}))

    # HANDSHAKE.v1
    def hs_sign(p: dict)->dict: return {"attestation_id":_hash(p),"timestamp":int(time.time())}
    def hs_verify(p: dict)->dict: return {"verified":True,"fingerprint":_hash(p)}
    reg.register(Protocol("HANDSHAKE.v1",{"handshake.sign":hs_sign,"handshake.verify":hs_verify}))

    # WALLET.v1 (stub)
    def wl_request(p: dict)->dict: return {"method":p.get("method","unknown"),"amount":p.get("amount",0),"status":"requested"}
    def wl_record(p: dict)->dict: return {"txid":_hash(p),"status":"recorded"}
    reg.register(Protocol("WALLET.v1",{"wallet.request":wl_request,"wallet.record":wl_record}))

    # SCROLL_LICENSE.v1
    def lc_issue(p: dict)->dict: return {"license_id":_hash(p),"watermark":p.get("watermark",True)}
    def lc_revoke(p: dict)->dict: return {"revoked":True,"license_id":p.get("license_id","")}
    reg.register(Protocol("SCROLL_LICENSE.v1",{"license.issue":lc_issue,"license.revoke":lc_revoke}))

    # SAFEGUARD.v1
    def sg_profile(p: dict)->dict: return {"profile":p.get("level","balanced"),"throttle":p.get("throttle",False)}
    reg.register(Protocol("SAFEGUARD.v1",{"safeguard.profile":sg_profile}))

    # BEACON.v1
    def bc_broadcast(p: dict)->dict: return {"message":p.get("message",""),"status":"broadcast"}
    reg.register(Protocol("BEACON.v1",{"beacon.broadcast":bc_broadcast}))
    return reg

# ──────────────────────────────────────────────────────────────────────────────
# ACTIVATE
# ──────────────────────────────────────────────────────────────────────────────
def activate(codex_text: str = "") -> Router:
    tokens = extract_codex_tokens(codex_text or "")
    pl = PersonaLoader()
    for p in personas_from_codex(tokens): pl.register(p)
    pr = make_protocols()
    tb = ToolBox()
    tb.register("uppercase", lambda s: s.upper())
    tb.register("lowercase", lambda s: s.lower())
    tb.register("slug", lambda s: re.sub(r'[^a-z0-9]+','-', s.strip().lower()).strip('-'))
    tb.register("bullets_from_lines", lambda s: "\n".join(f"- {l}" for l in s.splitlines() if l.strip()))
    router = Router(pl, pr, tb, tokens)
    pl.load("Strategist")
    return router

# ──────────────────────────────────────────────────────────────────────────────
# DEMO when run directly (optional)
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample_codex = "!ZEUS !YGGDRASIL !LOVECRAFTIAN"
    shell = activate(sample_codex)
    print(shell.handle("!persona list"))
    print(shell.handle("monetize AI art app"))
    print(shell.handle('!protocol IVP.v1 ivp.create {"offer":"Pack","price_tiers":[0,29,99]}'))
