"""Tests for the bounded Omega HTC synthetic simulation."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.omega_htc_sim import objective, run_simulation, verify_ledger


class OmegaHtcSimulationTests(unittest.TestCase):
    def test_objective_has_known_optimum(self) -> None:
        self.assertEqual(objective(0.73, 0.27), 1.0)
        self.assertLess(objective(0.0, 0.0), 1.0)

    def test_same_seed_reproduces_search_result(self) -> None:
        first = run_simulation(cycles=5, max_evaluations=31, seed=42)
        second = run_simulation(cycles=5, max_evaluations=31, seed=42)
        self.assertEqual(first["best_candidate"], second["best_candidate"])
        self.assertEqual(first["evaluations"], second["evaluations"])
        self.assertEqual(first["cycle_results"], second["cycle_results"])

    def test_budget_is_bounded_and_expands_by_cycle(self) -> None:
        report = run_simulation(cycles=8, max_evaluations=17, seed=7)
        self.assertEqual(report["evaluations"], 17)
        self.assertLessEqual(report["evaluations"], 17)
        self.assertEqual([item["budget"] for item in report["cycle_results"]], [1, 2, 4, 8, 2])

    def test_ledger_appends_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "events.jsonl"
            first = run_simulation(cycles=2, max_evaluations=3, seed=11, ledger_path=ledger)
            self.assertEqual(first["ledger_records_after"], 3)
            second = run_simulation(cycles=1, max_evaluations=2, seed=12, ledger_path=ledger)
            # One cycle has a budget of 2**0 = 1, regardless of the higher ceiling.
            self.assertEqual(second["ledger_records_before"], 3)
            self.assertEqual(second["ledger_records_after"], 4)
            count, head = verify_ledger(ledger)
            self.assertEqual(count, 4)
            self.assertEqual(head, second["ledger_head_hash"])

    def test_ledger_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "events.jsonl"
            run_simulation(cycles=1, max_evaluations=1, seed=11, ledger_path=ledger)
            record = json.loads(ledger.read_text(encoding="utf-8"))
            record["score"] = -999
            ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Record hash mismatch"):
                verify_ledger(ledger)

    def test_invalid_limits_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            run_simulation(cycles=0)
        with self.assertRaises(ValueError):
            run_simulation(max_evaluations=0)


if __name__ == "__main__":
    unittest.main()
