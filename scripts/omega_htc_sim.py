#!/usr/bin/env python3
"""Bounded Hyperbolic Time Chamber (HTC) parameter-search simulation.

This is a deterministic, synthetic optimization harness. It does not connect to
real nodes, execute generated code, or accelerate physical time. Its expanding
per-cycle budget models an accelerated experiment schedule only.

Python standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "conzetian.omega_htc.record.v1"
ZERO_HASH = "0" * 64


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_record(record: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in record.items() if key != "record_hash"}
    return hashlib.sha256(canonical_json(unsigned).encode("utf-8")).hexdigest()


def verify_ledger(path: Path) -> tuple[int, str]:
    """Verify JSONL hash-chain integrity; return record count and final hash."""
    if not path.exists():
        return 0, ZERO_HASH

    previous = ZERO_HASH
    count = 0
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                raise ValueError(f"Blank ledger line at {line_number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at ledger line {line_number}") from exc
            if record.get("schema") != SCHEMA:
                raise ValueError(f"Unsupported schema at ledger line {line_number}")
            if record.get("prev_hash") != previous:
                raise ValueError(f"Broken previous-hash link at ledger line {line_number}")
            actual = digest_record(record)
            if record.get("record_hash") != actual:
                raise ValueError(f"Record hash mismatch at ledger line {line_number}")
            previous = actual
            count += 1
    return count, previous


def objective(x: float, y: float) -> float:
    """Synthetic bounded objective with a known optimum at (0.73, 0.27)."""
    return 1.0 - (x - 0.73) ** 2 - (y - 0.27) ** 2


def append_record(path: Path, payload: dict[str, Any], previous_hash: str) -> str:
    record = dict(payload)
    record["prev_hash"] = previous_hash
    record["record_hash"] = digest_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json(record) + "\n")
        stream.flush()
        import os
        os.fsync(stream.fileno())
    return record["record_hash"]


def run_simulation(
    cycles: int = 6,
    max_evaluations: int = 256,
    seed: int = 1680,
    ledger_path: Path | None = None,
) -> dict[str, Any]:
    if cycles < 1 or cycles > 20:
        raise ValueError("cycles must be between 1 and 20")
    if max_evaluations < 1 or max_evaluations > 100_000:
        raise ValueError("max_evaluations must be between 1 and 100000")

    rng = random.Random(seed)
    ledger_count, previous_hash = verify_ledger(ledger_path) if ledger_path else (0, ZERO_HASH)
    best: dict[str, float] | None = None
    evaluations = 0
    cycle_results: list[dict[str, Any]] = []
    started = datetime.now(timezone.utc).isoformat()

    for cycle in range(cycles):
        remaining = max_evaluations - evaluations
        if remaining <= 0:
            break
        budget = min(2 ** cycle, remaining)
        radius = max(0.025, 0.5 / (2 ** max(0, cycle - 1)))
        cycle_best = None

        for _ in range(budget):
            if best is None or rng.random() < 0.25:
                x, y = rng.random(), rng.random()
            else:
                x = min(1.0, max(0.0, rng.gauss(best["x"], radius)))
                y = min(1.0, max(0.0, rng.gauss(best["y"], radius)))
            score = objective(x, y)
            evaluations += 1
            candidate = {"x": x, "y": y, "score": score}
            if best is None or score > best["score"]:
                best = candidate
            if cycle_best is None or score > cycle_best["score"]:
                cycle_best = candidate

            if ledger_path:
                previous_hash = append_record(
                    ledger_path,
                    {
                        "schema": SCHEMA,
                        "record_type": "synthetic_evaluation",
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "seed": seed,
                        "cycle": cycle + 1,
                        "evaluation": evaluations,
                        "candidate": {"x": x, "y": y},
                        "score": score,
                        "best_score_to_date": best["score"],
                        "mode": "SIMULATION_ONLY",
                    },
                    previous_hash,
                )

        cycle_results.append({
            "cycle": cycle + 1,
            "budget": budget,
            "cycle_best_score": cycle_best["score"] if cycle_best else None,
            "best_score_to_date": best["score"] if best else None,
        })

    assert best is not None
    final_ledger_count, final_ledger_hash = (
        verify_ledger(ledger_path) if ledger_path else (0, ZERO_HASH)
    )
    return {
        "status": "SIMULATION_COMPLETED",
        "mode": "SYNTHETIC_OBJECTIVE_ONLY",
        "started_at_utc": started,
        "seed": seed,
        "cycles_requested": cycles,
        "cycles_completed": len(cycle_results),
        "evaluations": evaluations,
        "best_candidate": best,
        "known_optimum": {"x": 0.73, "y": 0.27, "score": 1.0},
        "absolute_score_gap": abs(1.0 - best["score"]),
        "cycle_results": cycle_results,
        "ledger_path": str(ledger_path) if ledger_path else None,
        "ledger_records_before": ledger_count,
        "ledger_records_after": final_ledger_count,
        "ledger_head_hash": final_ledger_hash,
        "limitations": [
            "Synthetic benchmark; no real system or decentralized node was accessed.",
            "Expanding budgets simulate an accelerated schedule; no physical time is accelerated.",
            "A valid hash chain detects many edits but does not prove a record's claims are true.",
            "This harness optimizes two synthetic parameters, not general intelligence or global capability.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=6)
    parser.add_argument("--max-evaluations", type=int, default=256)
    parser.add_argument("--seed", type=int, default=1680)
    parser.add_argument("--ledger", type=Path, default=None,
                        help="Optional append-only JSONL ledger path; existing chain is verified first.")
    args = parser.parse_args(argv)
    try:
        report = run_simulation(args.cycles, args.max_evaluations, args.seed, args.ledger)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
