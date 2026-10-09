import json
import tempfile
import unittest
from pathlib import Path

from scripts.omega_federation_sim import objective, run_simulation


class FederationSimulationTests(unittest.TestCase):
    def test_objective_known_optimum(self):
        self.assertEqual(objective(0.73, 0.27), 1.0)

    def test_simulation_is_reproducible_except_timestamps(self):
        a = run_simulation(agents=4, rounds=8, seed=1680)
        b = run_simulation(agents=4, rounds=8, seed=1680)
        self.assertEqual(a["best_candidate"], b["best_candidate"])
        self.assertEqual(a["agent_states"], b["agent_states"])
        self.assertEqual(a["ledger_records_this_run"], 8)
        self.assertEqual(a["mode"], "SYNTHETIC_OBJECTIVE_ONLY")

    def test_limits_are_enforced(self):
        with self.assertRaises(ValueError):
            run_simulation(agents=33)
        with self.assertRaises(ValueError):
            run_simulation(rounds=101)

    def test_ledger_appends_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "events.jsonl"
            run_simulation(agents=2, rounds=2, seed=7, ledger_path=str(path))
            run_simulation(agents=2, rounds=1, seed=8, ledger_path=str(path))
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[2]["prev_hash"], rows[1]["record_hash"])
            rows[0]["round"] = 99
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            with self.assertRaises(ValueError):
                run_simulation(agents=2, rounds=1, seed=8, ledger_path=str(path))


if __name__ == "__main__":
    unittest.main()
