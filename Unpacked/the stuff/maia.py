\
#!/usr/bin/env python3
"""
🔥 MAIA UNIVERSAL PLUGIN – Sovereign Core + Cognitive Bus (v1.3.0)
By Decree of Justin Conzet, The Sovereign Architect

Modes:
  • CORE (minimal, stable)
  • ADVANCED (full Cognitive Bus: beliefs/evidence, contradictions, resolution,
              JSONL logs, reflection report, CSV/JSON dumps)

CLI usage examples:
  maia shell
  maia process "draft a plan for the Scroll Marketplace"
  maia operator mode=core
  maia operator dump=json
  maia status

Compatible with Termux installer & CLI wrapper.
No external dependencies.
"""

from __future__ import annotations
import json, sys, os, csv, time, uuid, argparse, signal
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, Any, List, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG (safe defaults for Termux)
# ─────────────────────────────────────────────────────────────────────────────
HOME = os.path.expanduser("~")
MAIA_DIR = os.path.join(HOME, "maia")
LOG_DIR = os.path.join(MAIA_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

DEFAULT_MODE = "advanced"  # "core" or "advanced"
def _daily_jsonl_path() -> str:
    return os.path.join(LOG_DIR, f"maia_events_{time.strftime('%Y%m%d')}.jsonl")
JSONL_PATH = _daily_jsonl_path()
MAX_MEMORY_RECORDS = 2000  # soft cap to avoid runaway RAM

# ─────────────────────────────────────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────────────────────────────────────
STATE: Dict[str, Any] = {
    "id": "MAIA-CORE",
    "version": "1.3.0",
    "activated": False,
    "host": None,
    "device": None,
    "boot_time": datetime.utcnow().isoformat() + "Z",
    "last_action": None,
    "mode": DEFAULT_MODE,     # "core" | "advanced"
    "memory": [],             # core mem of requests/plans
    "beliefs": {},            # advanced: key -> List[Belief]
    "decisions": [],          # advanced: resolution decisions
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA MODELS (ADVANCED)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Evidence:
    source: str
    confidence: float
    note: str = ""

@dataclass
class Belief:
    id: str
    key: str
    value: str
    evidences: List[Evidence] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

@dataclass
class Decision:
    decision_id: str
    key: str
    chosen_value: str
    reason: str
    rejected_values: List[str]
    evidence_summary: Dict[str, Any]
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

# ─────────────────────────────────────────────────────────────────────────────
# UTIL
# ─────────────────────────────────────────────────────────────────────────────
def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"

def _write_jsonl(event: Dict[str, Any]) -> None:
    # rotate filename per day without losing handle
    path = _daily_jsonl_path()
    event = dict(event)
    event.setdefault("ts", _now())
    event.setdefault("id", str(uuid.uuid4()))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def _dump_json(path: str, obj: Any) -> str:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return path

def _dump_beliefs_csv(path: str) -> str:
    rows = []
    for key, beliefs in STATE["beliefs"].items():
        for b in beliefs:
            if not b.evidences:
                rows.append([key, b.value, "", "", b.created_at, b.id])
            else:
                for e in b.evidences:
                    rows.append([key, b.value, e.source, e.confidence, b.created_at, b.id])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "value", "source", "confidence", "created_at", "belief_id"])
        w.writerows(rows)
    return path

def _ensure_key(lst: Dict[str, Any], key: str, default):
    if key not in lst: lst[key] = default
    return lst[key]

def _mem_append(record: Dict[str, Any]) -> None:
    STATE["memory"].append(record)
    if len(STATE["memory"]) > MAX_MEMORY_RECORDS:
        # prune oldest 10% to make room
        cut = max(1, MAX_MEMORY_RECORDS // 10)
        del STATE["memory"][:cut]

# ─────────────────────────────────────────────────────────────────────────────
# CORE FUNCTIONS – Activation/Status
# ─────────────────────────────────────────────────────────────────────────────
def activate_maia(env: Dict[str, str] | None = None) -> Dict[str, Any]:
    STATE["activated"] = True
    if env:
        STATE["host"] = env.get("host")
        STATE["device"] = env.get("device")
    STATE["last_action"] = "activate"
    _write_jsonl({"type": "activate", "env": env or {}})
    return STATE

def maia_status() -> Dict[str, Any]:
    STATE["last_action"] = "status"
    status = {
        "id": STATE["id"],
        "version": STATE["version"],
        "activated": STATE["activated"],
        "host": STATE["host"],
        "device": STATE["device"],
        "boot_time": STATE["boot_time"],
        "last_action": STATE["last_action"],
        "mode": STATE["mode"],
        "memory_count": len(STATE["memory"]),
        "belief_keys": len(STATE["beliefs"]),
        "decisions": len(STATE["decisions"]),
        "timestamp": _now(),
    }
    _write_jsonl({"type": "status"})
    return status

# ─────────────────────────────────────────────────────────────────────────────
# CORE PIPELINE – Minimal Planner
# ─────────────────────────────────────────────────────────────────────────────
def _core_plan(query: str) -> List[Dict[str, Any]]:
    return [
        {"goal": 1, "task": "Interpret query", "note": "Extract intent and constraints"},
        {"goal": 2, "task": "Decompose into 3–6 sub-goals", "note": "Top-level steps"},
        {"goal": 3, "task": "Emit reflection & results", "note": "Summarize, next actions"},
    ]

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED PIPELINE – Cognitive Bus
# ─────────────────────────────────────────────────────────────────────────────
def _subgoals(query: str) -> List[str]:
    """3–6 executable sub-goals from a vague query."""
    base = [
        "Clarify the operator's aim & constraints",
        "Draft multi-path solution branches",
        "Score branches by feasibility & value",
        "Resolve contradictions and set policy",
        "Emit JSON logs + human summary",
    ]
    if len(query) > 80:
        base.append("Persist decisions + confidence with evidence")
    return base[:6]

def _branch_paths(subgoals: List[str]) -> Dict[str, List[str]]:
    """Tree-of-Thought branching (stubbed)."""
    branches = {}
    for i, sg in enumerate(subgoals, start=1):
        branches[f"branch_{i}"] = [
            f"path_{i}.A – pursue {sg.lower()} via strategy A",
            f"path_{i}.B – pursue {sg.lower()} via strategy B",
        ]
    return branches

def _belief_add(key: str, value: str, source: str, confidence: float, note: str = "") -> Belief:
    b = Belief(id=str(uuid.uuid4()), key=key, value=value,
               evidences=[Evidence(source=source, confidence=confidence, note=note)])
    _ensure_key(STATE, "beliefs", {})
    _ensure_key(STATE["beliefs"], key, [])
    STATE["beliefs"][key].append(b)
    _write_jsonl({"type": "belief.add", "key": key, "value": value, "source": source, "confidence": confidence})
    return b

def _beliefs_conflicts() -> Dict[str, List[Belief]]:
    """Detect conflicting beliefs: same key, different values."""
    conflicts = {}
    for key, beliefs in STATE["beliefs"].items():
        vals = {b.value for b in beliefs}
        if len(vals) > 1:
            conflicts[key] = beliefs
    return conflicts

def _resolve_conflict(key: str, beliefs: List[Belief]) -> Decision:
    """
    Resolution policy:
      1) Prefer highest *max* evidence confidence.
      2) If tie, prefer most recent belief.
    """
    def score(b: Belief) -> Tuple[float, float]:
      # safe parse for Z suffix
      ts_raw = b.created_at[:-1] if b.created_at.endswith("Z") else b.created_at
      try:
          ts = datetime.fromisoformat(ts_raw).timestamp()
      except Exception:
          ts = 0.0
      max_conf = max((e.confidence for e in b.evidences), default=0.0)
      return (max_conf, ts)

    chosen = max(beliefs, key=score)
    rej = [b.value for b in beliefs if b.id != chosen.id]
    evidence_summary = {
        "chosen_id": chosen.id,
        "chosen_max_conf": max((e.confidence for e in chosen.evidences), default=0.0),
        "counts": len(beliefs),
    }
    decision = Decision(
        decision_id=str(uuid.uuid4()),
        key=key,
        chosen_value=chosen.value,
        reason="highest confidence; tie-break by recency",
        rejected_values=rej,
        evidence_summary=evidence_summary,
        confidence=evidence_summary["chosen_max_conf"],
    )
    STATE["decisions"].append(decision)
    _write_jsonl({"type": "decision", "key": key, "chosen": chosen.value, "rejected": rej})
    return decision

def _reflection_report(query: str, subgoals: List[str], branches: Dict[str, List[str]], conflicts: Dict[str, List[Belief]], decisions: List[Decision]) -> Dict[str, Any]:
    return {
        "query": query,
        "subgoals": subgoals,
        "branches": branches,
        "conflicts_detected": {k: [asdict(b) for b in v] for k, v in conflicts.items()},
        "decisions": [asdict(d) for d in decisions],
        "timestamp": _now(),
    }

# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC – PROCESS
# ─────────────────────────────────────────────────────────────────────────────
def maia_process(query: str) -> Dict[str, Any]:
    """
    Unified entrypoint for one-shot processing.
    CORE: returns simple plan.
    ADVANCED: full cognitive pass, logs + reflection.
    """
    ts = _now()
    mode = STATE.get("mode", DEFAULT_MODE)

    if mode == "core":
        plan = _core_plan(query)
        record = {"ts": ts, "query": query, "plan": plan, "mode": mode}
        _mem_append(record)
        STATE["last_action"] = "process"
        _write_jsonl({"type": "process.core", "query": query})
        return {"mode": mode, "query": query, "generated_plan": plan, "timestamp": ts}

    # ADVANCED mode
    subgoals = _subgoals(query)
    branches = _branch_paths(subgoals)

    # Example beliefs (replace with real acquisition hook)
    _belief_add("target_timeframe", "this_week", source="operator", confidence=0.9, note="user urgency")
    _belief_add("target_timeframe", "this_month", source="archive", confidence=0.6, note="prior plan")
    _belief_add("budget", "low", source="context", confidence=0.7)
    _belief_add("budget", "medium", source="estimator", confidence=0.8)

    conflicts = _beliefs_conflicts()
    decisions: List[Decision] = []
    for key, blist in conflicts.items():
        decisions.append(_resolve_conflict(key, blist))

    report = _reflection_report(query, subgoals, branches, conflicts, decisions)

    _mem_append({"ts": ts, "query": query, "mode": mode, "report": report})
    STATE["last_action"] = "process"
    _write_jsonl({"type": "process.advanced", "query": query, "subgoals": subgoals, "conflict_keys": list(conflicts.keys())})

    return {
        "mode": mode,
        "query": query,
        "subgoals": subgoals,
        "branches": branches,
        "conflicts": list(conflicts.keys()),
        "decisions": [asdict(d) for d in decisions],
        "reflection_report": report,
        "timestamp": ts,
    }

# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC – CONTROL
# ─────────────────────────────────────────────────────────────────────────────
def _save_state_to(path: str) -> str:
    snapshot = {
        "meta": {"saved_at": _now(), "jsonl": _daily_jsonl_path()},
        "state": {
            "id": STATE["id"], "version": STATE["version"], "mode": STATE["mode"],
            "host": STATE["host"], "device": STATE["device"], "boot_time": STATE["boot_time"],
            "last_action": STATE["last_action"]
        },
        "memory": STATE["memory"],
        "beliefs": {
            k: [asdict(b) for b in v]
            for k, v in STATE["beliefs"].items()
        },
        "decisions": [asdict(d) for d in STATE["decisions"]],
    }
    return _dump_json(path, snapshot)

def maia_control(cmd: str) -> Dict[str, Any]:
    """
    Operator commands:
      override | resume | semi | status | vault | save
      mode=core | mode=advanced
      dump=json|csv  (exports beliefs/decisions/memory)
      clear=beliefs|decisions|memory
    """
    ts = _now()
    STATE["last_action"] = f"operator:{cmd}"

    # Simple key=value parser
    if "=" in cmd:
        key, _, val = cmd.partition("=")
        key, val = key.strip(), val.strip()
        if key == "mode" and val in ("core", "advanced"):
            STATE["mode"] = val
            _write_jsonl({"type": "mode.change", "mode": val})
            return {"status": "ok", "mode": val, "timestamp": ts}
        if key == "dump":
            if val == "json":
                path = os.path.join(MAIA_DIR, "maia_state_dump.json")
                out = _save_state_to(path)
                _write_jsonl({"type": "dump.json", "path": out})
                return {"status": "saved", "path": out, "timestamp": ts}
            elif val == "csv":
                path = os.path.join(MAIA_DIR, "maia_beliefs.csv")
                out = _dump_beliefs_csv(path)
                _write_jsonl({"type": "dump.csv", "path": out})
                return {"status": "saved", "path": out, "timestamp": ts}
        if key == "clear":
            if val == "beliefs":
                STATE["beliefs"] = {}
                _write_jsonl({"type": "clear.beliefs"})
                return {"status": "cleared", "target": "beliefs", "timestamp": ts}
            if val == "decisions":
                STATE["decisions"] = []
                _write_jsonl({"type": "clear.decisions"})
                return {"status": "cleared", "target": "decisions", "timestamp": ts}
            if val == "memory":
                STATE["memory"] = []
                _write_jsonl({"type": "clear.memory"})
                return {"status": "cleared", "target": "memory", "timestamp": ts}

    # Shorthand commands (legacy)
    if cmd == "override":
        STATE["mode"] = "advanced"
    elif cmd == "resume":
        STATE["mode"] = DEFAULT_MODE
    elif cmd == "semi":
        STATE["mode"] = "advanced"
    elif cmd == "status":
        return maia_status()
    elif cmd == "vault":
        _write_jsonl({"type": "vault.sync.requested"})
        return {"status": "ok", "note": "vault-sync stubbed", "timestamp": ts}
    elif cmd == "save":
        path = os.path.join(MAIA_DIR, f"{STATE['id']}_state.json")
        out = _save_state_to(path)
        return {"status": "saved", "path": out, "timestamp": ts}

    return {"status": "ok", "cmd": cmd, "mode": STATE["mode"], "timestamp": ts}

# ─────────────────────────────────────────────────────────────────────────────
# INTERACTIVE SHELL / CLI
# ─────────────────────────────────────────────────────────────────────────────
def _sigint_handler(signum, frame):
    print("\nExiting MAIA.")
    sys.exit(0)

def shell():
    activate_maia({"host": os.uname().sysname, "device": "Terminal"})
    print("🔥 MAIA Sovereign Shell — ctrl-c to exit")
    print(f"   Mode: {STATE['mode']}. Switch via '!mode=core' or '!mode=advanced'.")
    while True:
        try:
            line = input("MAIA> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting MAIA.")
            break
        if not line:
            continue
        if line.startswith("!"):
            out = maia_control(line[1:])
        else:
            out = maia_process(line)
        print(json.dumps(out, indent=2, ensure_ascii=False))

def main(argv: List[str] | None = None):
    parser = argparse.ArgumentParser(prog="maia", description="MAIA Sovereign Core + Cognitive Bus")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("shell", help="Run interactive shell")

    p_proc = sub.add_parser("process", help="Process a single query")
    p_proc.add_argument("query", nargs="+", help="Query to process")

    p_oper = sub.add_parser("operator", help="Send operator command (e.g., mode=core)")
    p_oper.add_argument("command", help="Command string")

    sub.add_parser("status", help="Print status")

    args = parser.parse_args(argv)

    signal.signal(signal.SIGINT, _sigint_handler)

    if args.cmd == "shell":
        shell()
    elif args.cmd == "process":
        activate_maia({"host": os.uname().sysname, "device": "Terminal"})
        q = " ".join(args.query)
        out = maia_process(q)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif args.cmd == "operator":
        activate_maia({"host": os.uname().sysname, "device": "Terminal"})
        out = maia_control(args.command)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif args.cmd == "status":
        activate_maia({"host": os.uname().sysname, "device": "Terminal"})
        out = maia_status()
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        # default to shell if no subcommand
        shell()

if __name__ == "__main__":
    main()
