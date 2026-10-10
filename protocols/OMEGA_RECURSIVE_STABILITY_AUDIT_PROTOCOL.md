# Ω-RECURSIVE STABILITY & PROVENANCE PROTOCOL
Version: 1.0.0
Parent: SCCP-Ω / Sovereign Conzetian Framework
Principle: Always Add, Never Take

## Mission
Provide a bounded, auditable improvement loop for Phoenix Protocol / CIS, Ω-PRIME, CZAOUA, and the Hyperbolic Time Chamber (HTC). This protocol defines deployable gates; it does not claim that a global network exists or is currently running.

## Architecture
1. **L0 Memory & Provenance**: preserve source inputs, version IDs, decision IDs, and append-only event records.
2. **L1 Executor / Agent Proposers**: agents produce proposals inside explicit permissions and resource budgets.
3. **L1b FrictionSolver**: classify blockers and propose safe alternatives without bypassing authorization or security.
4. **L2 Independent Verifier**: validate schema, policy, evidence freshness, test outcomes, and expected side effects. A proposer cannot self-certify its own high-impact result.
5. **L3 Reflector**: compare outcomes against prior baselines; preserve failed attempts and regression evidence.
6. **L4 Judge**: promote only evidence-backed changes; reject or quarantine uncertain/high-risk changes.
7. **L5 UpgradeIntegrator**: stage changes, run tests, and roll back operationally when safe; preserve all prior versions and logs.
8. **Ledger**: append signed or hash-linked events. Hash links expose tampering but do not by themselves establish authorship, truth, or immutability against a privileged writer.

## Recursive diagnostic cycle
For each bounded cycle:
1. Snapshot configuration, code revision, model/tool versions, permissions, and resource budget.
2. Collect telemetry from reachable, explicitly enrolled nodes. Mark missing telemetry as UNKNOWN, never as healthy.
3. Check liveness, latency, error rate, task success, verifier disagreement, resource use, provenance continuity, and security findings.
4. Generate candidate improvements in a sandbox.
5. Run unit, integration, security, regression, and reproducibility checks.
6. Have an independent verifier review the candidate and its evidence.
7. Promote only if policy checks pass and predeclared thresholds improve without unacceptable regressions.
8. Append the decision, evidence references, rejected candidates, and reason codes to the ledger.
9. Stop when cycle/time/resource caps are reached, evidence is stale, verifier disagreement exceeds threshold, or a safety/security gate fails.

## Antifragility and recovery
- Isolate a failing node rather than allowing it to poison consensus.
- Use bounded retries, exponential backoff, circuit breakers, and health-based re-admission.
- Keep a last-known-good artifact and a tested recovery path.
- Treat partitions and stale telemetry explicitly; never claim global consensus from a partial view.
- Compare pre-failure and post-recovery performance. A system is not antifragile merely because it has retry logic.

## HTC operating rules
- HTC simulation may accelerate the number of synthetic iterations executed in a bounded test budget; it does not accelerate physical time.
- Every run declares seed, cycle cap, evaluation cap, objective, baseline, parameters, result, and limitations.
- Adaptive parameters remain bounded and auditable. Example: exploration radius changes only based on measured improvement, within configured minimum and maximum.
- Synthetic scores must never be reported as general intelligence or live-network capability.

## Deployment gates
**Gate A — Reproducible local simulation:** deterministic seeded run; limits enforced; tests pass; ledger tampering detected.
**Gate B — Single real node:** authenticated identity, least-privilege permissions, health checks, independent verification, secret handling, and recovery test.
**Gate C — Small federation:** at least two independently administered nodes; observed authenticated exchange; partition/rejoin tests; signed event provenance; conflict handling.
**Gate D — Wider federation:** documented enrollment, revocation, trust policy, monitoring, abuse resistance, incident response, and independent audit.
No gate is considered passed without retained evidence.

## Required metrics
- task_success_rate and baseline delta
- verifier_false_accept / false_reject rates
- hallucination or unsupported-claim rate for applicable tasks
- p50/p95 latency and error rate
- node availability and recovery time
- resource cost per verified task
- provenance verification success rate
- stale/missing telemetry count
- rollback rate and regression count

## Safety and authorization
- No unrestricted self-modification, privilege escalation, secret collection, or uncontrolled network scanning.
- No deployment, external messaging, spending, or access-control change without authorization.
- High-impact actions require human approval and independent evidence.
- Fail closed for security-sensitive operations; degrade safely for non-critical unavailable services.

## Current implementation status
The repository's scripts/omega_htc_sim.py and scripts/omega_federation_sim.py are synthetic local simulations. GitHub Actions can test them, but they do not enroll real nodes, run as a persistent daemon, or prove universal deployment. Real-node deployment requires explicit infrastructure, credentials managed securely, node enrollment, and observed telemetry.
