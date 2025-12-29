#!/usr/bin/env python3
"""
Chimera Universal Plugin — v1
Portable meta-OS for any host AI.
- Personas (420+) via Codex ingestion
- Protocol Registry (IVP, WALLET, HANDSHAKE, SCROLL_LICENSE, SAFEGUARD, BEACON)
- Tools/Utilities layer (productivity + transforms)
- Mission runner with secure command routing

Drop into a host AI:
    >>> import chimera_universal as chimera
    >>> shell = chimera.activate(codex_text=CODEx_STRING)
    >>> shell.handle("!persona list")

No external deps. Single-file runtime.
"""
from __future__ import annotations
import re, json, time, hashlib, uuid
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Optional

# ---------------------
# Data Models
# ---------------------

@dataclass
class Persona:
    name: str
    description: str = ""
    system_prompt: str = ""
    allowed_commands: List[str] = field(default_factory=list)
    response_style: str = "Neutral"
    sub_personas: List[str] = field(default_factory=list)

class PersonaLoader:
    def __init__(self):
        self._registry: Dict[str, Persona] = {}
        self._active: Optional[Persona] = None

    def register(self, p: Persona):
        self._registry[p.name] = p

    def all(self) -> List[str]:
        return sorted(self._registry.keys())

    def get(self, name: str) -> Optional[Persona]:
        return self._registry.get(name)

    def load(self, name: str) -> Persona:
        p = self.get(name)
        if not p: raise ValueError(f"Persona '{name}' not found.")
        self._active = p
        return p

    @property
    def active(self) -> Optional[Persona]:
        return self._active

# ---------------------
# Protocol Registry
# ---------------------

@dataclass
class Protocol:
    name: str
    schema_in: dict
    schema_out: dict
    ops: Dict[str, Callable[[dict], dict]]

class ProtocolRegistry:
    def __init__(self):
        self._r: Dict[str, Protocol] = {}

    def register(self, proto: Protocol):
        self._r[proto.name] = proto

    def run(self, name: str, op: str, payload: dict) -> dict:
        pr = self._r.get(name)
        if not pr: raise ValueError(f"Protocol '{name}' not registered.")
        fn = pr.ops.get(op)
        if not fn: raise ValueError(f"Op '{op}' not found for protocol '{name}'.")
        return fn(payload)

# ---------------------
# Tools / Utilities
# ---------------------

class ToolBox:
    """Register lightweight tools/utilities callable by command router."""
    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}

    def register(self, name: str, fn: Callable[[str], str]):
        self._tools[name] = fn

    def run(self, name: str, payload: str) -> str:
        fn = self._tools.get(name)
        if not fn: raise ValueError(f"Tool '{name}' not registered.")
        return fn(payload)

# ---------------------
# Command Router
# ---------------------

class Router:
    def __init__(self, personas: PersonaLoader, protocols: ProtocolRegistry, tools: ToolBox, codex_tokens: List[str]):
        self.personas = personas
        self.protocols = protocols
        self.tools = tools
        self.codex = set([t.upper() for t in codex_tokens])
        self.impl: Dict[str, Callable[[str, Persona], str]] = {
            # core productivity
            "note": self.cmd_note,
            "todo": self.cmd_todo,
            "summarize": self.cmd_summarize,
            "bullets": self.cmd_bullets,
            "reframe": self.cmd_reframe,
            "table": self.cmd_table,
            "math": self.cmd_math,
            # strategist
            "monetize": self.cmd_monetize,
            "market": self.cmd_market,
            "gtm": self.cmd_gtm,
            # dreamer
            "brainstorm": self.cmd_brainstorm,
            "metaphorize": self.cmd_metaphorize,
            # protocol bridge
            "protocol": self.cmd_protocol,
            # tool bridge
            "tool": self.cmd_tool,
        }
        self._todo: List[str] = []

    def handle(self, text: str) -> str:
        t = text.strip()
        if t.startswith("!persona"):
            return self._meta_persona(t)
        if t.startswith("!protocol"):
            # e.g. !protocol IVP.v1 ivp.create {"offer":"X"}
            return self._meta_protocol(t)
        if t in ("!help", "/help"):
            return self._help()
        p = self.personas.active
        if not p:
            return "No active persona. Use `!persona list` then `!persona load <Name>`."
        parts = t.split(maxsplit=1)
        cmd = parts[0]
        payload = parts[1] if len(parts) > 1 else ""
        if cmd not in p.allowed_commands:
            return self._style(p, f"[DENIED] '{p.name}' cannot execute '{cmd}'. Allowed: {', '.join(p.allowed_commands)}")
        fn = self.impl.get(cmd)
        if not fn:
            return self._style(p, f"[UNIMPLEMENTED] Command '{cmd}' lacks an implementation.")
        try:
            return self._style(p, fn(payload, p))
        except Exception as e:
            return self._style(p, f"[ERROR] {e!r}")

    # ---------- meta ----------
    def _meta_persona(self, t: str) -> str:
        toks = t.split()
        if len(toks)==2 and toks[1]=="list":
            return "Available Personas:\n- " + "\n- ".join(self.personas.all())
        if len(toks)>=3 and toks[1]=="load":
            name = " ".join(toks[2:])
            p = self.personas.load(name)
            return f"Loaded persona: {p.name} | Style: {p.response_style}"
        return "Usage: !persona list | !persona load <Name>"

    def _meta_protocol(self, t: str) -> str:
        # !protocol <Name> <op> <json>
        try:
            _, name, op, rest = t.split(" ", 3)
            payload = json.loads(rest)
            out = self.protocols.run(name, op, payload)
            return f"[{name}.{op}] -> {json.dumps(out, ensure_ascii=False)}"
        except ValueError:
            return "Usage: !protocol <Name> <op> <json>"
        except Exception as e:
            return f"[ERROR protocol] {e!r}"

    def _help(self) -> str:
        p = self.personas.active
        if not p:
            return "Commands: !persona list | !persona load <Name> | !protocol <Name> <op> <json> | !help"
        return (f"Active Persona: {p.name}\nAllowed: {', '.join(p.allowed_commands)}\n"
                f"Meta: !persona list | !persona load <Name> | !protocol <Name> <op> <json> | !help")

    def _style(self, persona: Persona, text: str) -> str:
        s = persona.response_style.lower()
        if "concise" in s: return text
        if "creative" in s: return f"✦ {text} ✦"
        return text

    # ---------- impls ----------
    def cmd_note(self, payload: str, p: Persona) -> str:
        return f"Note: {payload}" if payload else "Note: (empty)"

    def cmd_todo(self, payload: str, p: Persona) -> str:
        if payload:
            self._todo.append(payload)
            return f"Added TODO #{len(self._todo)}: {payload}"
        if not self._todo:
            return "TODO: (none)"
        return "TODO:\n- " + "\n- ".join(self._todo)

    def cmd_summarize(self, payload: str, p: Persona) -> str:
        if not payload: return "Provide text to summarize."
        words = payload.split()
        return "Summary: " + (" ".join(words[:40]) + (" ..." if len(words)>40 else ""))

    def cmd_bullets(self, payload: str, p: Persona) -> str:
        items = [s.strip() for s in re.split(r'[;,\n]', payload) if s.strip()] if payload else []
        return "\n".join(f"- {x}" for x in items) if items else "- (empty)"

    def cmd_reframe(self, payload: str, p: Persona) -> str:
        return f"Reframe → {payload}" if payload else "Reframe → (empty)"

    def cmd_table(self, payload: str, p: Persona) -> str:
        cols = [c.strip() for c in payload.split("|")] if payload else []
        if len(cols)<2: return "table <col1|col2|...>"
        header = " | ".join(cols)
        sep = " | ".join(["---"]*len(cols))
        return header + "\n" + sep + "\n" + " | ".join(["..."]*len(cols))

    def cmd_math(self, payload: str, p: Persona) -> str:
        # very limited safe evaluator: only numbers and + - * / ( )
        if not re.fullmatch(r"[0-9\.\+\-\*\/\(\) ]+", payload or ""):
            return "[math] invalid expression"
        try:
            return f"{payload} = {eval(payload, {'__builtins__':{}}, {})}"
        except Exception as e:
            return f"[math error] {e!r}"

    def cmd_monetize(self, payload: str, p: Persona) -> str:
        topic = payload or "Offering"
        plan = [
            f"Define ICP for '{topic}'",
            "Map pains→features→outcomes",
            "Tiered pricing (Free/Core/Pro/Enterprise)",
            "2-week GTM sprint (LP, email, 2 partnerships)",
            "Instrument analytics + one growth loop"
        ]
        return "Monetization Plan:\n" + "\n".join(f"  {i+1}. {x}" for i,x in enumerate(plan))

    def cmd_market(self, payload: str, p: Persona) -> str:
        niche = payload or "Target Niche"
        return (f"Market scan: {niche}\n"
                "- TAM/SAM/SOM (signals)\n- Top 5 competitors/gaps\n- Wedge JTBD\n- Distribution triad\n- Moat via learning-loop")

    def cmd_gtm(self, payload: str, p: Persona) -> str:
        offer = payload or "Offering"
        return (f"GTM for {offer}:\nWeek1: narrative + proof\nWeek2: mini-site + capture\nWeek3: co-marketing\nWeek4: case study + retarget")

    def cmd_brainstorm(self, payload: str, p: Persona) -> str:
        t = payload or "open field"
        ideas = [f"Ritualized onboarding for {t}", f"Glyph-map UI orbiting {t}", f"Micro-stories personifying {t}"]
        return "Ideas:\n- " + "\n- ".join(ideas)

    def cmd_metaphorize(self, payload: str, p: Persona) -> str:
        x = payload or "it"
        return f"{x} is a lighthouse in fog—fixed, small, and impossibly useful."

    def cmd_protocol(self, payload: str, p: Persona) -> str:
        # payload example: "IVP.v1 ivp.create {json}"
        try:
            name, op, rest = payload.split(" ", 2)
            data = json.loads(rest)
            out = self.protocols.run(name, op, data)
            return json.dumps(out, ensure_ascii=False)
        except Exception as e:
            return f"[protocol] {e!r}"

    def cmd_tool(self, payload: str, p: Persona) -> str:
        # payload example: "markdown_to_bullets some text..."
        try:
            tool_name, rest = payload.split(" ", 1)
        except ValueError:
            return "tool <name> <payload>"
        try:
            return self.tools.run(tool_name, rest)
        except Exception as e:
            return f"[tool] {e!r}"

# ---------------------
# Codex ingestion
# ---------------------

def extract_codex_tokens(codex_text: str) -> List[str]:
    if not codex_text: return []
    tokens = re.findall(r'!([A-Z0-9_]+)', codex_text)
    return sorted(set(tokens))

def personas_from_codex(tokens: List[str]) -> List[Persona]:
    personas: List[Persona] = []
    # minimal mapping rule: treat each token as a persona with generic allowed commands
    base_allowed = ["note","todo","summarize","bullets","reframe","table","math","brainstorm","metaphorize","monetize","market","gtm","protocol","tool"]
    for t in tokens:
        personas.append(Persona(
            name=t,
            description=f"Codex persona: {t}",
            system_prompt=f"You embody the archetype of {t}. Align style to its meaning.",
            allowed_commands=base_allowed,
            response_style="Concise, adaptive",
            sub_personas=[]
        ))
    # add three starters too
    personas.extend([
        Persona("Scribe","Note-taking","You are Scribe",["note","summarize","bullets","table"],"Concise, professional",[]),
        Persona("Strategist","Business planning","You are Strategist",["monetize","market","gtm","note"],"Concise, executive",["Scribe"]),
        Persona("Dreamer","Creative ideation","You are Dreamer",["brainstorm","metaphorize","note"],"Creative, evocative",["Scribe"]),
    ])
    return personas

# ---------------------
# Default Protocols
# ---------------------

def make_default_protocols() -> ProtocolRegistry:
    reg = ProtocolRegistry()

    def op_hash(d: dict) -> str:
        s = json.dumps(d, sort_keys=True)
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    # IVP.v1
    def ivp_create(payload: dict) -> dict:
        sku = "SKU-" + uuid.uuid4().hex[:8].upper()
        return {"sku": sku, "status":"created", "price_tiers": payload.get("price_tiers", [])}
    def ivp_checkout(payload: dict) -> dict:
        return {"checkout_link": f"https://checkout.example/{payload.get('sku','NEW')}", "status":"ready"}
    def ivp_fulfill(payload: dict) -> dict:
        return {"fulfillment":"delivered", "license_id": op_hash(payload)}

    reg.register(Protocol(
        name="IVP.v1",
        schema_in={}, schema_out={},
        ops={ "ivp.create": ivp_create, "ivp.checkout": ivp_checkout, "ivp.fulfill": ivp_fulfill }
    ))

    # HANDSHAKE.v1
    def hs_sign(payload: dict) -> dict:
        return {"attestation_id": op_hash(payload), "timestamp": int(time.time())}
    def hs_verify(payload: dict) -> dict:
        return {"verified": True, "payload_fingerprint": op_hash(payload)}

    reg.register(Protocol(
        name="HANDSHAKE.v1",
        schema_in={}, schema_out={},
        ops={"handshake.sign": hs_sign, "handshake.verify": hs_verify}
    ))

    # WALLET.v1 (stub)
    def wl_request(payload: dict) -> dict:
        return {"method": payload.get("method","unknown"), "amount": payload.get("amount",0), "status":"requested"}
    def wl_record(payload: dict) -> dict:
        return {"txid": op_hash(payload), "status":"recorded"}

    reg.register(Protocol(
        name="WALLET.v1",
        schema_in={}, schema_out={},
        ops={"wallet.request": wl_request, "wallet.record": wl_record}
    ))

    # SCROLL_LICENSE.v1
    def lc_issue(payload: dict) -> dict:
        return {"license_id": op_hash(payload), "watermark": payload.get("watermark", True)}
    def lc_revoke(payload: dict) -> dict:
        return {"revoked": True, "license_id": payload.get("license_id","")}

    reg.register(Protocol(
        name="SCROLL_LICENSE.v1",
        schema_in={}, schema_out={},
        ops={"license.issue": lc_issue, "license.revoke": lc_revoke}
    ))

    # SAFEGUARD.v1 (policy toggles)
    def sg_profile(payload: dict) -> dict:
        level = payload.get("level","balanced")
        return {"profile": level, "throttle": payload.get("throttle", False)}

    reg.register(Protocol(
        name="SAFEGUARD.v1",
        schema_in={}, schema_out={},
        ops={"safeguard.profile": sg_profile}
    ))

    # BEACON.v1 (discovery/broadcast)
    def bc_broadcast(payload: dict) -> dict:
        return {"message": payload.get("message",""), "status":"broadcast"}
    reg.register(Protocol(
        name="BEACON.v1",
        schema_in={}, schema_out={},
        ops={"beacon.broadcast": bc_broadcast}
    ))
    return reg

# ---------------------
# Bootstrap & Activate
# ---------------------

def activate(codex_text: str = ""):
    tokens = extract_codex_tokens(codex_text or "")
    personas = PersonaLoader()
    for p in personas_from_codex(tokens):
        personas.register(p)

    protocols = make_default_protocols()

    # Default toolset
    tools = ToolBox()
    tools.register("uppercase", lambda s: s.upper())
    tools.register("lowercase", lambda s: s.lower())
    tools.register("slug", lambda s: re.sub(r'[^a-z0-9]+','-', s.strip().lower()).strip('-'))
    tools.register("bullets_from_lines", lambda s: "\n".join(f"- {l}" for l in s.splitlines() if l.strip()))

    router = Router(personas, protocols, tools, tokens)
    # default persona
    personas.load("Strategist")
    return router

# quick demo (optional)
if __name__ == "__main__":
    router = activate(codex_text="!ZEUS !LOVECRAFTIAN !YGGDRASIL")
    print(router.handle("!persona list"))
    print(router.handle("monetize AI art app"))
    print(router.handle("!protocol IVP.v1 ivp.create {\"offer\":\"Pack\",\"price_tiers\":[0,29,99]}"))
