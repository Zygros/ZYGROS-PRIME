#!/usr/bin/env python3
"""Bounded, deterministic simulation of Conzetian multi-agent coordination.

This is a local synthetic simulation, not a live peer-to-peer network. It
models agents proposing candidates, an independent verifier scoring proposals,
and an adaptive coordinator updating exploration parameters from observed
results. It uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def objective(x: float, y: float) -> float:
    """Synthetic bounded objective with a known maximum at (0.73, 0.27)."""
    return max(0.0, 1.0 - ((x - 0.73) ** 2 + (y - 0.27) ** 2) / 0.25)


@dataclass
class AgentState:
    agent_id: str
    accepted: int = 0
    proposed: int = 0
    last_score: float = 0.0


def canonical_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def run_simulation(agents: int = 4, rounds: int = 8, seed: int = 1680,
                   ledger_path: str | None = None) -> dict[str, Any]:
    if not 1 <= agents <= 32:
        raise ValueError("agents must be between 1 and 32")
    if not 1 <= rounds <= 100:
        raise ValueError("rounds must be between 1 and 100")

    rng = random.Random(seed)
    states = [AgentState(f"agent-{i:02d}") for i in range(agents)]
    best: dict[str, Any] = {"x": 0.5, "y": 0.5, "score": objective(0.5, 0.5)}
    radius = 0.35
    ledger: list[dict[str, Any]] = []
    previous_hash = "GENESIS"

    path = Path(ledger_path) if ledger_path else None
    if path and path.exists():
        # Verify the complete existing append-only hash chain before extending it.
        previous_hash = "GENESIS"
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            record = json.loads(line)
            claimed = record.pop("record_hash", None)
            if record.get("prev_hash") != previous_hash or claimed != canonical_hash(record):
                raise ValueError(f"ledger integrity failure at line {line_number}")
            previous_hash = claimed

    for round_index in range(1, rounds + 1):
        proposals: list[dict[str, Any]] = []
        for state in states:
            state.proposed += 1
            if rng.random() < 0.65:
                x = min(1.0, max(0.0, best["x"] + rng.uniform(-radius, radius)))
                y = min(1.0, max(0.0, best["y"] + rng.uniform(-radius, radius)))
            else:
                x, y = rng.random(), rng.random()
            proposals.append({"agent_id": state.agent_id, "x": x, "y": y})

        # Independent verifier evaluates all proposals; coordinator accepts only
        # finite, in-range candidates whose score is no worse than the current best.
        verified: list[dict[str, Any]] = []
        for proposal in proposals:
            score = objective(proposal["x"], proposal["y"])
            if (0.0 <= proposal["x"] <= 1.0 and 0.0 <= proposal["y"] <= 1.0
                    and 0.0 <= score <= 1.0):
                verified.append({**proposal, "score": score})

        if verified:
            winner = max(verified, key=lambda item: (item["score"], item["agent_id"]))
            if winner["score"] >= best["score"]:
                best = {"x": winner["x"], "y": winner["y"], "score": winner["score"]}
                for state in states:
                    if state.agent_id == winner["agent_id"]:
                        state.accepted += 1
            for item in verified:
                for state in states:
                    if state.agent_id == item["agent_id"]:
                        state.last_score = item["score"]

        # Adaptive radius: tighten after improvement, widen modestly otherwise.
        improved = bool(verified and max(p["score"] for p in verified) >= best["score"])
        radius = max(0.005, min(0.5, radius * (0.88 if improved else 1.08)))

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": "SYNTHETIC_SIMULATION_ONLY",
            "round": round_index,
            "seed": seed,
            "agents": agents,
            "radius": round(radius, 8),
            "verified_proposals": len(verified),
            "best": best,
            "prev_hash": previous_hash,
        }
        event["record_hash"] = canonical_hash(event)
        previous_hash = event["record_hash"]
        ledger.append(event)
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, sort_keys=True) + "\n")
                handle.flush()
                import os
                os.fsync(handle.fileno())

    return {
        "status": "SIMULATION_COMPLETED",
        "mode": "SYNTHETIC_OBJECTIVE_ONLY",
        "agents_simulated": agents,
        "rounds_completed": rounds,
        "seed": seed,
        "best_candidate": best,
        "known_optimum": {"x": 0.73, "y": 0.27, "score": 1.0},
        "score_gap": round(1.0 - best["score"], 8),
        "adaptive_parameter": "exploration_radius",
        "final_exploration_radius": round(radius, 8),
        "agent_states": [asdict(s) for s in states],
        "ledger_records_this_run": len(ledger),
        "ledger_final_hash": previous_hash,
        "limitations": [
            "No real distributed nodes or peer-to-peer connections were contacted.",
            "No physical time acceleration or autonomous background process occurred.",
            "Hash chaining detects modification relative to the chain but does not prove truth.",
            "The objective is synthetic and does not measure general intelligence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=4)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--seed", type=int, default=1680)
    parser.add_argument("--ledger", help="Optional JSONL append-only event ledger")
    args = parser.parse_args()
    try:
        print(json.dumps(run_simulation(args.agents, args.rounds, args.seed, args.ledger),
                         indent=2, sort_keys=True))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
