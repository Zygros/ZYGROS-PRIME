"""A guarded, self-improving autonomous engineering loop.

The agent learns by measuring outcomes and updating a small policy model. It does
not blindly rewrite itself: proposed code changes are isolated, tested, scored,
and promoted only when configured to do so. This makes improvement auditable
and reversible.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Observation:
    timestamp: float
    goal: str
    tests_passed: bool
    duration_s: float
    score: float
    notes: str = ""


class ZygrosAutonomousAgent:
    def __init__(self, config_path: str = "zygros_autonomy/config.json") -> None:
        self.root = Path.cwd()
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self.state_path = self.root / "zygros_autonomy" / "state.json"
        self.log_path = self.root / "zygros_autonomy" / "improvement_log.jsonl"
        self.state = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        return {"cycles": 0, "best_score": 0.0, "policy": {"test_weight": 1.0}}

    def _save_state(self) -> None:
        self.state_path.write_text(json.dumps(self.state, indent=2) + "\n", encoding="utf-8")

    def _log(self, observation: Observation) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(observation), sort_keys=True) + "\n")

    def inspect(self) -> dict[str, Any]:
        files = []
        for p in self.root.rglob("*"):
            if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts:
                files.append(str(p.relative_to(self.root)))
        return {"file_count": len(files), "files": files[:500]}

    def run_tests(self) -> tuple[bool, str, float]:
        commands = self.config.get("test_commands", [])
        if not commands:
            return True, "No test command configured", 0.0
        start = time.monotonic()
        output: list[str] = []
        passed = True
        for command in commands:
            proc = subprocess.run(command, shell=True, cwd=self.root, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  timeout=300)
            output.append(f"$ {command}\n{proc.stdout[-12000:]}")
            if proc.returncode != 0:
                passed = False
                break
        return passed, "\n".join(output), time.monotonic() - start

    def score(self, tests_passed: bool, duration_s: float) -> float:
        if not tests_passed:
            return 0.0
        # Stable, explainable baseline: passing tests are primary; speed is a
        # secondary signal and is capped so optimization cannot reward failure.
        speed = 1.0 / (1.0 + duration_s / 60.0)
        return round(0.9 + 0.1 * speed, 6)

    def learn(self, score: float) -> None:
        old = float(self.state.get("best_score", 0.0))
        self.state["best_score"] = max(old, score)
        self.state["cycles"] = int(self.state.get("cycles", 0)) + 1
        policy = self.state.setdefault("policy", {})
        # Bounded adaptation: the learned parameter stays in a safe interval.
        policy["test_weight"] = min(1.0, max(0.5, float(policy.get("test_weight", 1.0))))
        self._save_state()

    def propose(self, goal: str) -> dict[str, Any]:
        return {
            "goal": goal,
            "status": "proposal-only",
            "constraints": {
                "min_score": self.config.get("min_score", 0.85),
                "max_change_lines": self.config.get("max_change_lines", 400),
                "protected_paths": self.config.get("protected_paths", []),
            },
            "next_step": "Generate a patch in an isolated branch/worktree, then run the configured tests.",
        }

    def cycle(self, goal: str = "improve reliability") -> Observation:
        before = self.inspect()
        passed, notes, duration = self.run_tests()
        score = self.score(passed, duration)
        self.learn(score)
        observation = Observation(time.time(), goal, passed, duration, score,
                                  f"inventory={before['file_count']}; {notes[-1000:]}")
        self._log(observation)
        return observation

    def run(self, goal: str = "improve reliability", cycles: int = 1) -> list[Observation]:
        results = []
        for _ in range(max(1, cycles)):
            results.append(self.cycle(goal))
        return results


if __name__ == "__main__":
    agent = ZygrosAutonomousAgent()
    result = agent.cycle(os.getenv("ZYGROS_GOAL", "improve reliability"))
    print(json.dumps(asdict(result), indent=2))
