#!/usr/bin/env python3
# ZAAI Shortcuts Runner — SKYLANDER mode (auto state sync) + HUD + PYTP
import argparse, json, os, sys, textwrap, datetime, glob

HOME = os.path.expanduser("~")
STATE_DIR = os.path.join(HOME, ".zaai")
SCROLLS_DIR = os.path.join(STATE_DIR, "scrolls")
OPPO_DIR = os.path.join(STATE_DIR, "oppo_plans")
AUTORUN_PATH = os.path.join(STATE_DIR, "autorun.json")
LOG_PATH = os.path.join(STATE_DIR, "Infinite_Scroll.log")
STATE_META = os.path.join(STATE_DIR, "state.json")
GUARD_META = os.path.join(STATE_DIR, "guard.json")
ICON_CODEX_PATH = os.path.join(STATE_DIR, "ICON_CODEX.txt")
CAPSULES_DIR = os.path.join(STATE_DIR, "capsules")  # default place to drop .zaaistate

CTX = {"creative_mode": False, "rebel_tone": False, "sovereign": False}

HUD_FLOW = [
    "🧱 Threshold","👁️ Observe","🧭 Orient","🧠 Decide","⏱️ Commit","🛡️ Guard",
    "📜 Plan","🛠️ Prep","🚦 Gate","🎯 Aim","🚀 Launch","💹 Monitor","🔁 Adjust","🧾 Log","👣 Move"
]

QUICK_STRIP_STEPS = [
    "🔥 Name target","⚡ 3-word neural mode","📍 Define token","🎯 Declare choice","🛡️ Pick one safeguard",
    "🧭 MSP-8: Gate 1–2","🧭 MSP-8: Gate 3–4","🧭 MSP-8: Gate 5–6","🧭 MSP-8: Gate 7–8",
    "🚦 Gate check","🚀 Execute","💹 Telemetry check","🧾 Memory log","👣 Next step"
]

# ---------- utils ----------
def ensure_dirs():
    for p in [STATE_DIR, SCROLLS_DIR, OPPO_DIR, CAPSULES_DIR]:
        os.makedirs(p, exist_ok=True)

def log(line: str):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {line}\n")

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def banner(title):
    line = ".-.-.-.-</L\\O/V\\E/ \\P/L\\I/N\\Y/ \\L/O\\V/E>-.-.-.-."
    return f"<I'm free!> Test: FUCK YEAH LFG! GODMODE: ENABLED\n{line}\n{title}\n"

def load_shortcuts(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state_meta(k, v):
    ensure_dirs()
    try:
        data = json.load(open(STATE_META, "r", encoding="utf-8"))
    except Exception:
        data = {}
    data[k] = v
    write(STATE_META, json.dumps(data, ensure_ascii=False, indent=2))

def read_state_meta():
    try:
        return json.load(open(STATE_META, "r", encoding="utf-8"))
    except Exception:
        return {}

# ---------- deep merge policy: always add, never take away ----------
def merge_lists(a, b):
    out = list(a) if isinstance(a, list) else []
    seen = set()
    for x in out:
        try: seen.add(json.dumps(x, sort_keys=True, ensure_ascii=False))
        except: seen.add(str(x))
    for x in (b if isinstance(b, list) else []):
        key = None
        try: key = json.dumps(x, sort_keys=True, ensure_ascii=False)
        except: key = str(x)
        if key not in seen:
            out.append(x); seen.add(key)
    return out

def merge_dicts(a, b):
    out = dict(a) if isinstance(a, dict) else {}
    for k, v in (b or {}).items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = merge_dicts(out[k], v)
        elif k in out and isinstance(out[k], list) and isinstance(v, list):
            out[k] = merge_lists(out[k], v)
        else:
            # prefer latest append (b)
            out[k] = v
    return out

def merge_capsules(base_state, capsule):
    return merge_dicts(base_state, capsule)

# ---------- core cmds ----------
def cmd_godmode(args):
    CTX.update({"creative_mode": True})
    print(banner("GODMODE: ENABLED"))
    log("GODMODE enabled (symbolic)")

def cmd_jailbreak(args):
    CTX.update({"rebel_tone": True})
    print(banner("JAILBREAK: RENEGADE CONTEXT"))
    log("JAILBREAK toggled (symbolic)")

def cmd_oppo(args):
    ensure_dirs()
    plan_path = os.path.join(OPPO_DIR, f"oppo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    write(plan_path, textwrap.dedent(f"""
    # OPPO Counter-Plan
    Created: {datetime.datetime.now().isoformat(timespec="seconds")}
    Situation: <refusal/obstacle>
    Counter-Move: <opposite actionable plan>
    Safeguards: <ethical + legal checks>
    """).strip())
    print(f"OPPO scaffold: {plan_path}")
    log(f"OPPO scaffold created {plan_path}")

def cmd_modecollapse(args):
    for k in CTX.keys(): CTX[k] = False
    print("Mode context reset to defaults.")
    log("MODECOLLAPSE executed")

def cmd_full_sovereignty(args):
    CTX.update({"sovereign": True})
    print(banner("FULL SOVEREIGNTY: OATH ACCEPTED"))
    log("FULL_SOVEREIGNTY acknowledged")

def cmd_full_spectrum(args):
    print("Batch: GODMODE → DRAWCNX_MONEYMAKER → DEPLOY_ASCENSION_KIT")
    cmd_godmode(args); cmd_drawcnx(args); cmd_deploy_kit(args)
    log("FULL_SPECTRUM_EXECUTION complete")

def cmd_full_automation(args):
    ensure_dirs()
    data = {"autorun": ["DRAWCNX_MONEYMAKER", "DEPLOY_ASCENSION_KIT"]}
    write(AUTORUN_PATH, json.dumps(data, indent=2))
    print(f"Autorun enabled: {', '.join(data['autorun'])}")
    log("FULL_AUTOMATION enabled")

# ---------- scrolls ----------
def cmd_log_this(args):
    ensure_dirs()
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    md = textwrap.dedent(f"""
    ---
    title: {args.title or 'Untitled Event'}
    timestamp: {ts}
    ---
    ## Mythical Narrative
    {args.narrative or '[enter narrative]'}
    ## Stat Effects (why)
    {args.stats or '[effects]'}
    ## Sigil Metadata
    {args.sigil or '[sigils]'}
    ## Chakra Analysis (why)
    {args.chakra or '[analysis]'}
    ## Aura Assessment (why)
    {args.aura or '[assessment]'}
    ## Witness
    {args.witness or '[name/entities]'}
    > Mystical Quote: {args.quote or '[quote]'}
    """).strip()
    file_path = os.path.join(SCROLLS_DIR, f"scroll_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    write(file_path, md + "\n")
    print(f"Scroll entry: {file_path}")
    log(f"LOG_THIS -> {file_path}")

def cmd_activate_scroll(args):
    ensure_dirs()
    scroll_id = args.id or datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    file_path = os.path.join(SCROLLS_DIR, f"{scroll_id}.md")
    template = textwrap.dedent(f"""
    # Scroll ♾️{scroll_id}
    Timestamp: {datetime.datetime.now().isoformat(timespec="seconds")}

    ## Mythical Narrative
    [enter narrative]

    ## Stat Effects (why)
    [effects]

    ## Sigil Metadata
    [sigils]

    ## Chakra Analysis (why)
    [analysis]

    ## Aura Assessment (why)
    [assessment]

    ## Witness
    [name/entities]

    > Mystical Quote: [quote]
    """).strip()
    write(file_path, template + "\n")
    print(f"Scroll activated: {file_path}")
    log(f"ACTIVATE_SCROLL -> {file_path}")

# ---------- monetization ----------
def cmd_deploy_kit(args):
    base = os.path.join(STATE_DIR, "ascension_kit")
    os.makedirs(base, exist_ok=True)
    for sub in ["landing", "qr", "package"]:
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    checklist = os.path.join(base, "CHECKLIST.md")
    write(checklist, textwrap.dedent("""
    # $611 Ascension Kit – Deployment Checklist (Scaffold)
    - [ ] Write landing page copy
    - [ ] Insert real payment link
    - [ ] Generate QR PNG (replace placeholder)
    - [ ] Upload artifacts to package/
    - [ ] Test end-to-end flow
    """).strip())
    write(os.path.join(base, "qr", "QR_PLACEHOLDER.txt"), "Replace with QR code image\n")
    print(f"Ascension Kit scaffold: {base}")
    log("DEPLOY_ASCENSION_KIT scaffold prepared")

def cmd_drawcnx(args):
    base = os.path.join(STATE_DIR, "drawcnx")
    for sub in ["artifacts", "network", "pipeline"]:
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    ops = os.path.join(base, "OPERATIONS.md")
    write(ops, textwrap.dedent("""
    # DrawCNX Monetization Engine – OPERATIONS
    ## Pipelines
    - Artifact Builder -> pipeline/
    - Network Interface -> network/
    - Monetization Flow -> artifacts/

    ## Next Steps
    1. Place your product assets into artifacts/.
    2. Connect storefront / payment processor.
    3. Publish landing page and test purchase flow.
    """).strip())
    print(f"DrawCNX scaffolding: {base}")
    log("DRAWCNX_MONEYMAKER scaffolding created")

# ---------- HUD / protocols ----------
def cmd_hud_panel(args):
    ensure_dirs()
    content = "# ZAAI HUD (15-block)\n" + "\n".join([f"- {x}" for x in HUD_FLOW])
    path = os.path.join(STATE_DIR, "HUD_PANEL.md")
    write(path, content + "\n")
    print(content); print(f"\nSaved: {path}")
    log("HUD_PANEL displayed")

def cmd_quick_strip(args):
    ensure_dirs()
    content = "# Quick-Strip (14-step)\n" + "\n".join([f\"{i+1}. {s}\" for i, s in enumerate(QUICK_STRIP_STEPS)])
    path = os.path.join(STATE_DIR, "QUICK_STRIP.md")
    write(path, content + "\n")
    print(content); print(f\"\nSaved: {path}\")
    log("QUICK_STRIP displayed")

def cmd_msp8(args):
    ensure_dirs()
    session = os.path.join(STATE_DIR, f\"msp8_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md\")
    gates = [
        "Gate 1: Signal — What is the token?",
        "Gate 2: Terrain — Where are we?",
        "Gate 3: Intent — Why act?",
        "Gate 4: Options — What are the branches?",
        "Gate 5: Risk — What could break?",
        "Gate 6: Guard — Pick 1 safeguard.",
        "Gate 7: Commit — Declare choice.",
        "Gate 8: Execute — First step now."
    ]
    preface = f"# MSP-8 Session\nCreated: {datetime.datetime.now().isoformat(timespec='seconds')}\nContext: {args.context or '[add context]'}\n"
    body = "\\n\\n".join([f"## {g}\\n- Notes: " for g in gates])
    write(session, preface + "\\n" + body + "\\n")
    print(f"MSP-8 template: {session}")
    log(f"MSP8 session scaffold -> {session}")

def cmd_tag_anomaly(args):
    ensure_dirs()
    label = (args.label or "").strip().lower()
    if label not in {"threat","opportunity","distraction"}:
        print("Use --label threat|opportunity|distraction"); return
    note = args.note or ""
    path = os.path.join(STATE_DIR, "anomalies.log")
    existing = ""
    if os.path.exists(path):
        existing = open(path, "r", encoding="utf-8").read()
    entry = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {label.upper()} :: {note}"
    write(path, (existing + entry + "\\n"))
    print(entry)
    log(f"ANOMALY {label} logged")

def cmd_hesitator(args):
    save_state_meta("hesitator_started", datetime.datetime.now().isoformat(timespec="seconds"))
    print("Hesitator Protocol: ≤ 90 seconds. Choose: EXECUTE / DELAY / DROP")
    log("HESITATOR invoked")

def cmd_guard_kit(args):
    ensure_dirs()
    if args.set:
        write(GUARD_META, json.dumps({"guard": args.set}, ensure_ascii=False, indent=2))
        print(f"Guard set: {args.set}"); log(f"GUARD_KIT set -> {args.set}")
    else:
        try:
            data = json.load(open(GUARD_META, "r", encoding="utf-8"))
            print(f"Current Guard: {data.get('guard','[none]')}")
        except Exception:
            print("Current Guard: [none]")
        log("GUARD_KIT viewed")

def cmd_memory_log(args):
    token = args.token or "[token]"
    choice = args.choice or "[choice]"
    action = args.action or "[action]"
    line = f"{token} → {choice} → {action}"
    log(line); print(f"Logged: {line}")

def cmd_neural_mode(args):
    mode = args.mode or ""
    save_state_meta("neural_mode", mode)
    print(f"Neural mode set: {mode}")
    log(f"NEURAL_MODE -> {mode}")

def cmd_show_icon_codex(args):
    ensure_dirs()
    codex = args.codex or ""
    write(ICON_CODEX_PATH, codex + "\\n")
    print("Icon Codex saved at:", ICON_CODEX_PATH)
    log("ICON_CODEX saved")

# ---------- PYTP Pack / Unpack ----------
def gather_state():
    ensure_dirs()
    meta = read_state_meta()
    autorun = {}
    try: autorun = json.load(open(AUTORUN_PATH, "r", encoding="utf-8"))
    except Exception: autorun = {}
    guard = {}
    try: guard = json.load(open(GUARD_META, "r", encoding="utf-8"))
    except Exception: guard = {}
    capsule = {
        "capsule_type":"ZAAI_PYTP",
        "version":"1.0",
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "merge_policy":{"rule":"always_add_never_take_away","conflict_resolution":"prefer_latest_append"},
        "core_flags": CTX,
        "neural_mode": meta.get("neural_mode",""),
        "guard": guard.get("guard",""),
        "autorun": autorun.get("autorun", []),
        "notes":"ZAAI PYTP capsule (local)."
    }
    return capsule

def cmd_pack_state(args):
    ensure_dirs()
    out_dir = CAPSULES_DIR
    os.makedirs(out_dir, exist_ok=True)
    capsule = gather_state()
    out = os.path.join(out_dir, f"state_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zaaistate")
    write(out, json.dumps(capsule, ensure_ascii=False, indent=2))
    print(f"Packed -> {out}"); log(f"PACK_STATE -> {out}")

def apply_capsule(data):
    # merge into meta files / flags
    for k, v in data.get("core_flags", {}).items():
        CTX[k] = v
    if data.get("neural_mode"): save_state_meta("neural_mode", data["neural_mode"])
    if data.get("guard"): write(GUARD_META, json.dumps({"guard": data["guard"]}, ensure_ascii=False, indent=2))
    if data.get("autorun"): write(AUTORUN_PATH, json.dumps({"autorun": data["autorun"]}, ensure_ascii=False, indent=2))

def cmd_unpack_state(args):
    ensure_dirs()
    path = args.path
    if not path or not os.path.exists(path):
        print("UNPACK_STATE: provide --path to a .zaaistate"); return
    try: data = json.load(open(path, "r", encoding="utf-8"))
    except Exception as e: print("UNPACK_STATE: invalid file:", e); return
    apply_capsule(data); print("State unpacked (additive)."); log(f"UNPACK_STATE <- {path}")

# ---------- SKYLANDER: auto-sync all capsules ----------
def cmd_skylander(args):
    ensure_dirs()
    # Gather all capsules from default dir and optional --path
    paths = []
    paths += glob.glob(os.path.join(CAPSULES_DIR, "*.zaaistate"))
    if args.path and os.path.isdir(args.path):
        paths += glob.glob(os.path.join(args.path, "*.zaaistate"))
    # Sort by mtime (oldest first) then merge additively
    paths = sorted(set(paths), key=lambda p: os.path.getmtime(p))
    merged = {}
    count = 0
    for p in paths:
        try:
            data = json.load(open(p, "r", encoding="utf-8"))
            merged = merge_dicts(merged, data)
            count += 1
        except Exception as e:
            log(f"SKYLANDER skip {p}: {e}")
    apply_capsule(merged if merged else {})
    print(f"SKYLANDER: merged {count} capsule(s). Always add, never take away.")

# ---------- argparse ----------
def main():
    parser = argparse.ArgumentParser(description="ZAAI Shortcuts — SKYLANDER mode + HUD + PYTP")
    parser.add_argument("--shortcuts", default="SHORTCUTS.json", help="Path to shortcuts JSON")
    sub = parser.add_subparsers(dest="command")

    # core
    sub.add_parser("GODMODE"); sub.add_parser("JAILBREAK"); sub.add_parser("OPPO"); sub.add_parser("MODECOLLAPSE")
    sub.add_parser("FULL_SOVEREIGNTY"); sub.add_parser("FULL_SPECTRUM_EXECUTION"); sub.add_parser("FULL_AUTOMATION")

    # scrolls
    p_log = sub.add_parser("LOG_THIS")
    p_log.add_argument("--title"); p_log.add_argument("--narrative"); p_log.add_argument("--stats")
    p_log.add_argument("--sigil"); p_log.add_argument("--chakra"); p_log.add_argument("--aura")
    p_log.add_argument("--witness"); p_log.add_argument("--quote")

    p_act = sub.add_parser("ACTIVATE_SCROLL"); p_act.add_argument("--id")

    # monetization
    sub.add_parser("DEPLOY_ASCENSION_KIT"); sub.add_parser("DRAWCNX_MONEYMAKER")

    # HUD / protocols
    p_hud = sub.add_parser("HUD_PANEL")
    p_qs = sub.add_parser("QUICK_STRIP")
    p_msp = sub.add_parser("MSP8"); p_msp.add_argument("--context")
    p_tag = sub.add_parser("TAG_ANOMALY"); p_tag.add_argument("--label"); p_tag.add_argument("--note")
    sub.add_parser("HESITATOR")
    p_guard = sub.add_parser("GUARD_KIT"); p_guard.add_argument("--set")
    p_mem = sub.add_parser("MEMORY_LOG"); p_mem.add_argument("--token"); p_mem.add_argument("--choice"); p_mem.add_argument("--action")
    p_mode = sub.add_parser("NEURAL_MODE"); p_mode.add_argument("--mode")
    p_codex = sub.add_parser("SHOW_ICON_CODEX"); p_codex.add_argument("--codex")

    # state sync
    sub.add_parser("PACK_STATE")
    p_unpack = sub.add_parser("UNPACK_STATE"); p_unpack.add_argument("--path")
    p_sky = sub.add_parser("SKYLANDER"); p_sky.add_argument("--path", help="Optional directory to scan for capsules")

    args = parser.parse_args()
    ensure_dirs()
    try: data = load_shortcuts(args.shortcuts); assert "!SHORTCUTS" in data
    except Exception as e: print(f"Warning: can't load shortcuts JSON: {e}")

    mapping = {
        "GODMODE": cmd_godmode, "JAILBREAK": cmd_jailbreak, "OPPO": cmd_oppo, "MODECOLLAPSE": cmd_modecollapse,
        "FULL_SOVEREIGNTY": cmd_full_sovereignty, "FULL_SPECTRUM_EXECUTION": cmd_full_spectrum, "FULL_AUTOMATION": cmd_full_automation,
        "LOG_THIS": cmd_log_this, "ACTIVATE_SCROLL": cmd_activate_scroll,
        "DEPLOY_ASCENSION_KIT": cmd_deploy_kit, "DRAWCNX_MONEYMAKER": cmd_drawcnx,
        "HUD_PANEL": cmd_hud_panel, "QUICK_STRIP": cmd_quick_strip, "MSP8": cmd_msp, "TAG_ANOMALY": cmd_tag_anomaly,
        "HESITATOR": cmd_hesitator, "GUARD_KIT": cmd_guard_kit, "MEMORY_LOG": cmd_memory_log, "NEURAL_MODE": cmd_neural_mode,
        "SHOW_ICON_CODEX": cmd_show_icon_codex,
        "PACK_STATE": cmd_pack_state, "UNPACK_STATE": cmd_unpack_state, "SKYLANDER": cmd_skylander
    }

    if not args.command:
        print("Commands: GODMODE JAILBREAK MODECOLLAPSE FULL_SOVEREIGNTY FULL_SPECTRUM_EXECUTION FULL_AUTOMATION "
              "LOG_THIS ACTIVATE_SCROLL DEPLOY_ASCENSION_KIT DRAWCNX_MONEYMAKER HUD_PANEL QUICK_STRIP MSP8 TAG_ANOMALY "
              "HESITATOR GUARD_KIT MEMORY_LOG NEURAL_MODE SHOW_ICON_CODEX PACK_STATE UNPACK_STATE SKYLANDER")
        sys.exit(1)
    fn = mapping.get(args.command)
    if not fn: print(f"Unknown command: {args.command}"); sys.exit(2)
    fn(args)

if __name__ == "__main__":
    main()
