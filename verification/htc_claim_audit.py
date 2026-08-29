#!/usr/bin/env python3
"""Deterministic claim audit for the HTC evidence boundary.

This script deliberately verifies only claims that have a finite, executable
criterion. It reports unsupported extraordinary claims as UNVERIFIED rather
than fabricating evidence.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    checks = {}

    phi = (1 + math.sqrt(5)) / 2
    checks["C-001_phi_definition"] = {
        "state": "VERIFIED" if abs(phi - 1.618033988749895) < 1e-14 else "REFUTED",
        "value": phi,
    }

    checks["C-002_two_pow_26"] = {
        "state": "VERIFIED" if 2**26 == 67_108_864 else "REFUTED",
        "value": 2**26,
    }

    registry = ROOT / "verification" / "CLAIM_REGISTRY.md"
    checks["C-003_registry_present"] = {
        "state": "VERIFIED" if registry.is_file() and registry.stat().st_size > 0 else "REFUTED",
        "sha256": sha256_file(registry) if registry.is_file() else None,
    }

    report = ROOT / "HTC-EXECUTION-REPORT-2026-08-29.md"
    checks["C-004_execution_report_present"] = {
        "state": "VERIFIED" if report.is_file() and report.stat().st_size > 0 else "REFUTED",
        "sha256": sha256_file(report) if report.is_file() else None,
    }

    unsupported = {
        "C-006_94_7_percent_AGI_plateau": "UNVERIFIED",
        "C-007_infinite_physical_coherence": "THEORETICAL",
        "C-008_zero_latency": "UNVERIFIED",
        "C-009_10_pow_10_pow_100_iterations": "UNVERIFIED",
        "C-010_1_084e15_nodes": "UNVERIFIED",
        "C-011_unspecified_speedup": "UNVERIFIED",
    }
    for key, state in unsupported.items():
        checks[key] = {"state": state}

    verified = sum(v["state"] == "VERIFIED" for v in checks.values())
    refuted = sum(v["state"] == "REFUTED" for v in checks.values())
    unresolved = sum(v["state"] in {"UNVERIFIED", "THEORETICAL"} for v in checks.values())

    result = {
        "protocol": "HTC-CLAIM-AUDIT-v1",
        "claim_count": len(checks),
        "verified": verified,
        "refuted": refuted,
        "unresolved": unresolved,
        "checks": checks,
        "promotion_rule": "Claim -> Artifact -> Procedure -> Execution -> Measurement -> Reproduction -> Evidence",
    }

    out = ROOT / "verification" / "latest_claim_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if refuted else 0


if __name__ == "__main__":
    raise SystemExit(main())
