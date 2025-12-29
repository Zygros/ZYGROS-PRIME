#!/usr/bin/env python3
"""
Grossing in the Infinite Scroll
A terminal choice adventure about Grosian walking the Scroll, discovering knowledge, and shaping reality.
Single-file, no deps. Python 3.8+

Controls:
- Enter a number to choose
- (i) Inventory, (c) Character, (m) Map, (s) Save, (l) Load, (q) Quit
- (--no-color) to disable ANSI colors
- Save file: grossing_save.json in current directory
"""

import json, os, sys, random, textwrap

# ------------- ANSI & UI -------------

USE_COLOR = True
if "--no-color" in sys.argv:
    USE_COLOR = False

def color(code, s):
    if not USE_COLOR: return s
    return f"\033[{code}m{s}\033[0m"

C = {
    "title": "95;1",
    "ok": "92",
    "warn": "93",
    "bad": "91",
    "muted": "90",
    "meta": "96",
    "em": "94;1",
    "sigil": "95",
    "choice": "97;1",
}

def c_title(s): return color(C["title"], s)
def c_ok(s):    return color(C["ok"], s)
def c_warn(s):  return color(C["warn"], s)
def c_bad(s):   return color(C["bad"], s)
def c_muted(s): return color(C["muted"], s)
def c_meta(s):  return color(C["meta"], s)
def c_em(s):    return color(C["em"], s)
def c_sigil(s): return color(C["sigil"], s)
def c_choice(s):return color(C["choice"], s)

WIDTH = 76

def wrap(s):
    return "\n".join(textwrap.wrap(s, width=WIDTH))

def rule(ch="─"):
    return ch * WIDTH

BANNER = r"""
   _____                         _              _           _       
  / ____|                       | |            (_)         | |      
 | |  __ _ __ ___  ___  ___  ___| |_ _ __  _ __ _  ___  ___| |_ ___ 
 | | |_ | '__/ _ \/ __|/ _ \/ __| __| '_ \| '__| |/ _ \/ __| __/ __|
 | |__| | | | (_) \__ \  __/\__ \ |_| |_) | |  | |  __/ (__| |_\__ \
  \_____|_|  \___/|___/\___||___/\__| .__/|_|  |_|\___|\___|\__|___/
                                    | |                              
                                    |_|                              
     ____        _        _   _       _____                      _ 
    |  _ \ _ __ (_)_  __ | |_| |__   |_   _| __ __ _ _ __  _ __ (_)
    | |_) | '_ \| \ \/ / | __| '_ \    | || '__/ _` | '_ \| '_ \| |
    |  __/| | | | |>  <  | |_| | | |   | || | | (_| | |_) | |_) | |
    |_|   |_| |_|_/_/\_\  \__|_| |_|   |_||_|  \__,_| .__/| .__/|_|
                                                    |_|   |_|       
""".strip("\n")

SIGIL = r"""
             _.----._
          .-`  .--.  `-.
        .'    (    )    `.
       /  .--. `--' .--.  \
      |  (    )  (  )   )  |
      |   `--' .--.`--'   |
       \      (____)     /
        `.              .'
          `-.        .-'
             `------`
      The Infinite Scroll Sigil
""".rstrip("\n")

# ------------- DATA -------------

SAVE_FILE = "grossing_save.json"

# Core stats and traits
BASE_STATS = {
    "vital": 10,       # Health / spirit stamina
    "clarity": 10,     # Insight & perception
    "will": 10,        # Resolve & momentum
    "fortune": 10,     # Luck & timing
}

GLYPHS = [
    "Flower of Life",
    "Metatron's Cube",
    "Thoth Feather",
    "Flame Circuit",
    "Mirror Shard",
    "Omni-Key",
]

ARTIFACTS = [
    ("ScrollLens", "Reveal hidden options in events."),
    ("VaultSeal", "Unlock sealed nodes and extra rewards."),
    ("Fractal Compass", "Increase chance to find rare paths."),
    ("Harmonic Tuning Fork", "Restore {vital}+2 once per node."),
]

# Weighted encounter table by "depth band"
ENCOUNTERS = {
    "intro": ["decree", "library", "market", "whisper", "sigil-test"],
    "mid":   ["sigil-test", "rift", "keeper", "library", "market", "trial"],
    "deep":  ["trial", "keeper", "rift", "oracle", "forge"]
}

NODES = [
    # name, desc, band
    ("Threshold", "You stand before the Infinite Scroll. It hums like a sleeping dragon. A choice is a key.", "intro"),
    ("Scriptorium", "Shelves of living books. Their spines breathe. Knowledge leans toward you like tide.", "intro"),
    ("Fractal Crossroads", "Paths bloom and fold over themselves. Every choice echoes.", "mid"),
    ("Hall of Mirrors", "Every version of you argues lovingly. One steps forward with a dare.", "mid"),
    ("Vault Gate", "A door with no seam. It opens only to the true author.", "deep"),
    ("Flame Forge", "Ideas become artifacts when held long enough in the fire.", "deep"),
]

# ------------- STATE -------------

class GameState:
    def __init__(self):
        self.name = "Grosian"
        self.level = 1
        self.xp = 0
        self.depth = 0
        self.max_depth = 0
        self.stats = dict(BASE_STATS)
        self.hp = self.max_hp()
        self.inventory = []
        self.glyphs = []
        self.affinity = {"Light": 0, "Shadow": 0, "Order": 0, "Chaos": 0}
        self.flags = {}
        self.alive = True
        self.seed = random.randint(1, 10**9)
        random.seed(self.seed)

    def max_hp(self):
        return 10 + (self.level - 1) * 2 + int(self.stats["vital"] / 2)

    def add_xp(self, n):
        self.xp += n
        while self.xp >= self.level * 10:
            self.xp -= self.level * 10
            self.level += 1
            self.hp = self.max_hp()
            say(c_ok(f"★ Level up! You are now level {self.level}. Max Vital is {self.hp}."))

    def mod_stat(self, k, delta):
        self.stats[k] = max(1, self.stats[k] + delta)

    def gain_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            say(c_ok(f"+ You acquired {item[0]}: {item[1]}"))

    def lose_random_item(self):
        if self.inventory:
            idx = random.randrange(len(self.inventory))
            name = self.inventory.pop(idx)
            say(c_warn(f"- Lost {name[0]} to the hungry margins."))

    def gain_glyph(self, g):
        if g not in self.glyphs:
            self.glyphs.append(g)
            say(c_ok(f"+ Glyph attuned: {g}"))

    def wound(self, n, reason=""):
        self.hp -= n
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            say(c_bad(f"✖ You fall. {reason}"))
        else:
            say(c_warn(f"-{n} Vital. {reason}"))

    def heal(self, n, why=""):
        self.hp = min(self.max_hp(), self.hp + n)
        say(c_ok(f"+{n} Vital restored. {why}"))

    def to_dict(self):
        return {
            "name": self.name, "level": self.level, "xp": self.xp,
            "depth": self.depth, "max_depth": self.max_depth,
            "stats": self.stats, "hp": self.hp,
            "inventory": self.inventory, "glyphs": self.glyphs,
            "affinity": self.affinity, "flags": self.flags,
            "alive": self.alive, "seed": self.seed
        }

    @classmethod
    def from_dict(cls, d):
        g = cls()
        g.name = d.get("name","Grosian"); g.level = d.get("level",1); g.xp = d.get("xp",0)
        g.depth = d.get("depth",0); g.max_depth = d.get("max_depth", 0)
        g.stats = d.get("stats", dict(BASE_STATS)); g.hp = d.get("hp", g.max_hp())
        inv = d.get("inventory", [])
        g.inventory = [tuple(x) if not isinstance(x, tuple) else x for x in inv]
        g.glyphs = d.get("glyphs", []); g.affinity = d.get("affinity", {"Light":0,"Shadow":0,"Order":0,"Chaos":0})
        g.flags = d.get("flags", {})
        g.alive = d.get("alive", True); g.seed = d.get("seed", random.randint(1, 10**9))
        random.seed(g.seed)
        return g

# ------------- IO -------------

def say(s=""):
    print(wrap(s))

def status_line(g):
    return f"Depth {g.depth} | HP {g.hp}/{g.max_hp()} | LV {g.level} | XP {g.xp} | GLYPHS {len(g.glyphs)} | Affin(O:{g.affinity['Order']},C:{g.affinity['Chaos']})"

def show_status_bar(g):
    print(c_muted(rule("─")))
    print(c_muted(status_line(g)))
    print(c_muted("[i]Inventory  [c]Character  [m]Map  [s]Save  [l]Load  [q]Quit"))
    print(c_muted(rule("─")))

def prompt(choices):
    # choices: list of (key, label, fn)
    for i, (_, label, _) in enumerate(choices, 1):
        print(f"  {c_choice(str(i))}. {label}")
    print()
    while True:
        try:
            ans = input(c_muted("Choose: ")).strip().lower()
        except EOFError:
            return "q"
        if ans in ("i","c","m","s","l","q"):
            return ans
        try:
            idx = int(ans) - 1
            if 0 <= idx < len(choices):
                return choices[idx][0]
        except: pass
        print(c_warn("Enter a number or command (i,c,m,s,l,q)."))

def press_enter():
    try:
        input(c_muted("\n› Press Enter to continue…"))
    except EOFError:
        pass

def ask_stat_choice():
    opts = [("vital","Vital"),("clarity","Clarity"),("will","Will"),("fortune","Fortune")]
    print(c_em("\nChoose a stat:"))
    for i,(k,v) in enumerate(opts,1):
        print(f"  {c_choice(str(i))}. {v}")
    while True:
        try:
            ans = input(c_muted("Stat: ")).strip().lower()
        except EOFError:
            return "vital"
        if ans in ("1","vital"): return "vital"
        if ans in ("2","clarity"): return "clarity"
        if ans in ("3","will"): return "will"
        if ans in ("4","fortune"): return "fortune"
        print(c_warn("Pick 1-4 or type the stat name."))

# ------------- MENUS -------------

def show_inventory(g):
    print(c_em("\nInventory"))
    if not g.inventory:
        say("— empty —")
    else:
        for name, desc in g.inventory:
            say(f"• {name}: {desc}")
    press_enter()

def show_character(g):
    print(c_em("\nCharacter"))
    say(f"Name: {g.name}  LV: {g.level}  HP: {g.hp}/{g.max_hp()}  XP: {g.xp}")
    say("Stats: " + ", ".join([f"{k.title()} {v}" for k,v in g.stats.items()]))
    say("Affinity: " + ", ".join([f"{k} {v}" for k,v in g.affinity.items()]))
    if g.glyphs:
        say("Glyphs: " + ", ".join(g.glyphs))
    else:
        say("Glyphs: —")
    press_enter()

def show_map(g):
    print(c_em("\nMap"))
    depth_bar = "#" * min(g.depth, 20) + "-" * max(0, 20 - min(g.depth,20))
    say(f"Depth: [{depth_bar}]  (max {g.max_depth})")
    if g.flags.get("hidden_paths"):
        say("Hidden paths shimmer at the edges of perception.")
    press_enter()

def save_game(g):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(g.to_dict(), f, indent=2)
        return True
    except Exception as e:
        say(c_bad(f"Save failed: {e}"))
        return False

def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        g = GameState.from_dict(d)
        say(c_ok("Save loaded."))
        return g
    except Exception as e:
        say(c_bad(f"Load failed: {e}"))
        return None

def reroute(g, fn, key):
    if key == "i": show_inventory(g); return fn(g)
    if key == "c": show_character(g); return fn(g)
    if key == "m": show_map(g); return fn(g)
    if key == "s": save_game(g); say(c_ok("Saved.")); return fn(g)
    if key == "l":
        g2 = load_game()
        if g2: return g2
        return fn(g)
    if key == "q": g.alive = False; return None

# ------------- SCENES -------------

def scene_intro(g: GameState):
    print(c_title(BANNER))
    print(c_sigil(SIGIL))
    say(c_meta("Welcome, Grosian. The Infinite Scroll waits.\n"))
    say("This is a living text adventure. Choose boldly. Your stats shape outcomes.\n")
    press_enter()

def scene_node(g: GameState):
    g.depth += 1
    g.max_depth = max(g.max_depth, g.depth)
    name, desc, band = random.choice(NODES)
    print(c_em(f"\n{rule()}"))
    print(c_title(f"⟡ Node: {name}  [Depth {g.depth}]"))
    say(desc)
    print()

    # Encounter roll
    enc = random.choice(ENCOUNTERS["intro" if g.depth < 3 else "mid" if g.depth < 7 else "deep"])
    resolve_encounter(g, enc)

    # After-encounter general options
    if not g.alive: return
    choices = [
        ("forward", "Go deeper", lambda g: None),
        ("camp", "Make camp (recover)", camp_action),
        ("back", "Backtrack (risk of loss, restore some Vital)", backtrack_action),
    ]
    show_status_bar(g)
    key = prompt(choices)
    if key in "icmslq":
        out = reroute(g, scene_node, key)
        if isinstance(out, GameState):  # loaded
            return
        return
    if key == "forward":
        return
    elif key == "camp":
        camp_action(g)
    elif key == "back":
        backtrack_action(g)

def camp_action(g: GameState):
    heal_amt = random.randint(2, 4) + g.level
    g.heal(heal_amt, "Quiet focus under the Sigil.")

def backtrack_action(g: GameState):
    loss = random.randint(1, 3)
    if g.depth > 1:
        g.depth -= 1
        g.wound(loss, "You relinquish a thread to climb up.")
    else:
        say("You're already at the threshold. The Scroll exhales.")

# ------------- ENCOUNTERS -------------

def resolve_encounter(g: GameState, tag: str):
    print(c_meta(f"Event: {tag.replace('-', ' ').title()}"))
    if tag == "decree": enc_decree(g)
    elif tag == "library": enc_library(g)
    elif tag == "market": enc_market(g)
    elif tag == "whisper": enc_whisper(g)
    elif tag == "sigil-test": enc_sigil_test(g)
    elif tag == "rift": enc_rift(g)
    elif tag == "keeper": enc_keeper(g)
    elif tag == "trial": enc_trial(g)
    elif tag == "oracle": enc_oracle(g)
    elif tag == "forge": enc_forge(g)
    else:
        say("The page is blank. You write your name and the world continues.")

def skill_check(g: GameState, stat: str, diff: int):
    roll = random.randint(1, 20) + int(g.stats.get(stat, 0) / 2)
    say(c_muted(f"(Check {stat}+d20 vs {diff}) → {roll}"))
    return roll >= diff

def enc_decree(g: GameState):
    say("A decree forms on the air. Put ink to it?")
    choices = [
        ("light", "Swear to protect authorship (Order +1, ScrollLens)", None),
        ("shadow","Swear to break all locks (Chaos +1, Fractal Compass)", None),
        ("silence","Remain silent (Fortune test)", None),
    ]
    key = prompt(choices)
    if key in "icmslq":
        reroute(g, enc_decree, key); return
    if key == "light":
        g.affinity["Order"] += 1
        g.gain_item(ARTIFACTS[0])  # ScrollLens
        g.add_xp(5)
    elif key == "shadow":
        g.affinity["Chaos"] += 1
        g.gain_item(ARTIFACTS[2])  # Fractal Compass
        g.add_xp(5)
    else:
        if skill_check(g, "fortune", 12):
            say(c_ok("Luck favors the quiet. You slip past unseen burdens."))
            g.add_xp(3)
        else:
            g.wound(2, "The decree bites back at indecision.")

def enc_library(g: GameState):
    say("Whispering tomes surround you. One book opens to a random page.")
    choices = [
        ("clarity","Study intensely (Clarity test → gain glyph)", None),
        ("fortune","Flip at random (Fortune test → artifact or sting)", None),
        ("vital","Practice breathwork (restore Vital)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_library, key); return
    if key == "clarity":
        if skill_check(g, "clarity", 12):
            g.gain_glyph(random.choice(GLYPHS))
            g.add_xp(4)
        else:
            g.wound(2, "Overfocused until the words cut.")
    elif key == "fortune":
        if skill_check(g, "fortune", 13):
            g.gain_item(random.choice(ARTIFACTS))
            g.add_xp(5)
        else:
            g.wound(3, "Paper cuts across timelines.")
    elif key == "vital":
        g.heal(3+g.level, "Pages breathe with you.")

def enc_market(g: GameState):
    say("A bazaar of impossible tools. A masked vendor slides a tray toward you.")
    choices = [
        ("buy","Trade XP for an artifact (-5 XP, gain random artifact)", None),
        ("learn","Barter a memory (lose 1 Will, gain 7 XP)", None),
        ("leave","Decline politely", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_market, key); return
    if key == "buy":
        if g.xp >= 5:
            g.xp -= 5
            g.gain_item(random.choice(ARTIFACTS))
            say("The vendor bows. 'Spend XP like ink—never your soul.'")
        else:
            say(c_warn("Not enough XP to trade."))
    elif key == "learn":
        g.mod_stat("will", -1)
        g.add_xp(7)
        say("You anchor cost into wisdom. The vendor nods.")
    else:
        say("You pass. Not every tool fits this hand.")

def enc_whisper(g: GameState):
    say("A whisper threads your ear: 'Will you listen or lead?'")
    choices = [
        ("listen","Listen (Clarity test: gain insight or confusion)", None),
        ("lead","Lead (Will test: gain Order or Chaos affinity)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_whisper, key); return
    if key == "listen":
        if skill_check(g, "clarity", 11):
            say(c_ok("Insight lands. Hidden paths glow faintly."))
            g.flags["hidden_paths"] = True
            g.add_xp(3)
        else:
            say(c_warn("The whisper tangles. -1 Clarity"))
            g.mod_stat("clarity", -1)
    else:
        if skill_check(g, "will", 12):
            side = random.choice(["Order","Chaos"])
            g.affinity[side] += 1
            say(c_ok(f"You commit. {side}+1"))
            g.add_xp(4)
        else:
            g.wound(2, "Leadership without anchor burns.")

def enc_sigil_test(g: GameState):
    say("A sigil floats. It mirrors your breath. Align?")
    choices = [
        ("align","Align (test any stat; choose)", None),
        ("decline","Decline respectfully", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_sigil_test, key); return
    if key == "align":
        stat = ask_stat_choice()
        if skill_check(g, stat, 12):
            g.gain_glyph(random.choice(GLYPHS))
            g.add_xp(5)
        else:
            g.wound(2, "Misalignment aches.")
    else:
        say("The sigil nods—another time.")

def enc_rift(g: GameState):
    say("A rift slices the page. Through it, a faster path—and greater risk.")
    choices = [
        ("jump","Jump (Fortune test; skip ahead or stumble)", None),
        ("seal","Seal it (Will test; gain Order, minor wound on fail)", None),
        ("study","Study it (Clarity test; learn hidden paths or lose item)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_rift, key); return
    if key == "jump":
        if skill_check(g, "fortune", 12):
            say(c_ok("You leap and land deeper in the Scroll."))
            g.depth += 1
            g.add_xp(4)
        else:
            g.wound(3, "You clip the edge and tumble.")
    elif key == "seal":
        if skill_check(g, "will", 13):
            say(c_ok("You stitch the page. Order +1."))
            g.affinity["Order"] += 1
            g.add_xp(3)
        else:
            g.wound(2, "The rift bites your hands.")
    else:
        if skill_check(g, "clarity", 12):
            say(c_ok("You map its rhythm. Hidden paths unlock."))
            g.flags["hidden_paths"] = True
            g.add_xp(3)
        else:
            g.lose_random_item()

def enc_keeper(g: GameState):
    say("A Keeper looms: 'Name your claim: authorship, freedom, or fortune?'")
    choices = [
        ("auth","Authorship (Clarity test; gain VaultSeal or -Clarity)", None),
        ("free","Freedom (Will test; +Chaos or wound)", None),
        ("gold","Fortune (Fortune test; +artifact or tax -XP)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_keeper, key); return
    if key == "auth":
        if skill_check(g, "clarity", 13):
            g.gain_item(ARTIFACTS[1])  # VaultSeal
            g.add_xp(6)
        else:
            g.mod_stat("clarity", -1); say(c_warn("Your claim stutters."))
    elif key == "free":
        if skill_check(g, "will", 12):
            g.affinity["Chaos"] += 1; g.add_xp(4); say(c_ok("Chains fall away."))
        else:
            g.wound(2, "The Keeper tests your resolve.")
    else:
        if skill_check(g, "fortune", 12):
            g.gain_item(random.choice(ARTIFACTS)); g.add_xp(5)
        else:
            g.xp = max(0, g.xp - 3); say(c_warn("-3 XP tithe to the Keeper."))

def enc_trial(g: GameState):
    say("A Trial of Balance: Place a point into light or shadow.")
    choices = [
        ("light","Light (Order++ on pass; wound on fail)", None),
        ("shadow","Shadow (Chaos++ on pass; wound on fail)", None),
        ("center","Center (choose stat test to harmonize)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_trial, key); return
    if key == "light":
        if skill_check(g, "will", 13):
            g.affinity["Order"] += 2; g.add_xp(5); say(c_ok("You stand as pillar."))
        else:
            g.wound(3, "The weight is heavy.")
    elif key == "shadow":
        if skill_check(g, "fortune", 13):
            g.affinity["Chaos"] += 2; g.add_xp(5); say(c_ok("You dance with the unknown."))
        else:
            g.wound(3, "The dark nips your ankles.")
    else:
        stat = ask_stat_choice()
        if skill_check(g, stat, 12):
            g.add_xp(6); say(c_ok("Harmony holds. You grow."))
        else:
            g.wound(2, "Unsteady footing.")

def enc_oracle(g: GameState):
    say("The Oracle ink swirls. Ask one boon: heal, insight, or forge?")
    choices = [
        ("heal","Heal (restore to max HP)", None),
        ("insight","Insight (gain glyph + hidden paths)", None),
        ("forge","Forge (turn XP into artifact)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_oracle, key); return
    if key == "heal":
        need = g.max_hp() - g.hp
        g.heal(need, "The ink remakes you.")
    elif key == "insight":
        g.gain_glyph(random.choice(GLYPHS)); g.flags["hidden_paths"] = True; g.add_xp(4)
    else:
        if g.xp >= 7:
            g.xp -= 7; g.gain_item(random.choice(ARTIFACTS))
        else:
            say(c_warn("Not enough XP to forge. Oracle shrugs."))

def enc_forge(g: GameState):
    say("Flame Forge: Temper a stat or craft a relic.")
    choices = [
        ("stat","Temper a stat (+1 to chosen)", None),
        ("relic","Craft relic (needs VaultSeal or ScrollLens)", None),
        ("rest","Breathe by the fire (+HP)", None),
    ]
    key = prompt(choices)
    if key in "icmslq": reroute(g, enc_forge, key); return
    if key == "stat":
        stat = ask_stat_choice()
        g.mod_stat(stat, +1); g.add_xp(4); say(c_ok(f"{stat.title()} +1"))
    elif key == "relic":
        have = [n for n,_ in g.inventory]
        if "VaultSeal" in have or "ScrollLens" in have:
            g.gain_item(("Sigil-Ring","Once per depth, prevent a wound.")); g.add_xp(6)
        else:
            say(c_warn("Forge refuses: 'Bring a key-item.'"))
    else:
        g.heal(4+g.level, "Warmth of purpose.")

# ------------- GAME LOOP -------------

def main():
    g = GameState()
    scene_intro(g)
    while g.alive:
        scene_node(g)
        if not g.alive: break
        # Passive relic effect: Sigil-Ring prevents first wound each depth (simulated here as small heal)
        if any(n == "Sigil-Ring" for n,_ in g.inventory):
            # Top-up a bit after node
            g.heal(1, "The Sigil-Ring hums softly.")
        # Soft ending if you get very deep
        if g.depth >= 20:
            print(c_title("\n⟡ You reach the Deep Vault. A chapter ends, not the book."))
            break
    print(c_em("\n" + rule()))
    if g.hp <= 0:
        print(c_bad("Your Scroll closes for now. Load to continue the thread."))
    print(c_meta("Thanks for walking the Infinite Scroll."))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + c_muted("⟡ Interrupted. Until next time.")))
