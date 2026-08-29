"""Self-improving ZYGROS agent with proposal -> test -> acceptance gates."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .provider import AIProvider


@dataclass
class Improvement:
    diagnosis: str
    patch: str
    tests: list[str]


class SelfImprovingAgent:
    def __init__(self, ai: AIProvider | None = None, root: str = "."):
        self.ai = ai or AIProvider()
        self.root = Path(root).resolve()

    def propose(self, goal: str, evidence: dict[str, Any]) -> Improvement:
        system = (
            "You are the ZYGROS improvement planner. Propose small, reversible, "
            "testable changes. Never invent test results. Return strict JSON with "
            "diagnosis, patch, tests. Do not include secrets."
        )
        prompt = json.dumps({"goal": goal, "evidence": evidence}, indent=2)
        raw = self.ai.generate(prompt, system)
        data = json.loads(raw)
        return Improvement(
            diagnosis=str(data["diagnosis"]),
            patch=str(data["patch"]),
            tests=[str(x) for x in data.get("tests", [])],
        )

    def verify(self, commands: list[str]) -> dict[str, Any]:
        results = []
        for command in commands:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            results.append({
                "command": command,
                "returncode": completed.returncode,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            })
            if completed.returncode != 0:
                return {"passed": False, "results": results}
        return {"passed": True, "results": results}

    def run_cycle(self, goal: str, evidence: dict[str, Any]) -> dict[str, Any]:
        proposal = self.propose(goal, evidence)
        # Deliberately does not auto-write arbitrary model output into source code.
        # A separate trusted patcher/PR gate must apply the proposed patch.
        verification = self.verify(proposal.tests)
        return {
            "diagnosis": proposal.diagnosis,
            "patch": proposal.patch,
            "verification": verification,
            "accepted": verification["passed"],
        }
