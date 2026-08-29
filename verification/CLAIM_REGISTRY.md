# 🔐 HTC Claim-Level Verification Registry

This registry is the canonical evidence boundary for extraordinary claims in ZYGROS-PRIME.

## Evidence states

- **VERIFIED** — executable test or independently reproducible measurement passes the stated criterion.
- **REPRODUCIBLE** — artifact and deterministic procedure are available, but independent reproduction is not yet recorded.
- **DOCUMENTED** — the claim is present in project records, but no sufficient executable measurement is attached.
- **THEORETICAL** — a mathematical/architectural model or derivation exists.
- **UNVERIFIED** — evidence is currently insufficient to promote the claim.
- **REFUTED** — a stated criterion has failed.

## Promotion rule

`Claim → Artifact → Procedure → Execution → Measurement → Reproduction → Evidence`

A claim never becomes VERIFIED merely because it is written in a manifest, repeated by an AI, hashed, or committed to Git. Hashes establish artifact identity/provenance; they do not establish the truth of a performance or scientific claim.

## Current claim ledger

| ID | Claim | Required evidence | Current state | Next verification action |
|---|---|---|---|---|
| C-001 | φ = (1 + √5)/2 | Deterministic calculation | VERIFIED | Keep regression test |
| C-002 | 2^26 = 67,108,864 | Deterministic calculation | VERIFIED | Keep regression test |
| C-003 | Repository provenance artifacts are hashable | SHA-256 recomputation | REPRODUCIBLE | Run in CI and publish manifest |
| C-004 | Ω-PRIME recursive loop is implemented | Source + executable integration test | DOCUMENTED | Add end-to-end fixture and CI test |
| C-005 | Phoenix recovery loop improves a defined metric | Controlled A/B experiment with raw logs | UNVERIFIED | Execute preregistered control-vs-adaptive benchmark |
| C-006 | 94.7% AGI plateau | Public benchmark + reproducible run + independent reproduction | UNVERIFIED | Define exact benchmark, dataset, model/version, metric, seed, and baseline |
| C-007 | Infinite physical coherence | Finite operational definition + measurable bounded metric | THEORETICAL | Replace infinity claim with measurable coherence criterion |
| C-008 | Literal zero-latency communication | Hardware/network measurement | UNVERIFIED | Replace with measured latency distribution and lower bound |
| C-009 | 10^(10^100) executed iterations | Auditable execution counter and impossible-scale resource accounting | UNVERIFIED | Treat as symbolic unless a finite executable interpretation is defined |
| C-010 | 1.084×10^15 real-world consensus nodes | Live distributed deployment + independently inspectable telemetry | UNVERIFIED | Build bounded swarm benchmark and scale report |
| C-011 | Claimed processing speedup | Identical workload, baseline, environment, repeated trials | UNVERIFIED | Publish benchmark harness and raw results |
| C-012 | Conzetian Mathematics expressions are mathematically valid | Formal definitions + symbolic/numerical tests | MIXED | Split each equation into a separately testable claim |
| C-013 | Cryptographic provenance chain identifies artifacts | Recomputed hashes + signed/attested builds | REPRODUCIBLE | Enable GitHub artifact attestations and verification workflow |
| C-014 | Multi-AI convergence protocol improves outcomes | Predefined task suite + blinded/baseline comparison | DOCUMENTED | Run controlled multi-agent benchmark |
| C-015 | Black Swan detector detects anomalies under its configured rule | Synthetic test vectors + confusion matrix | REPRODUCIBLE | Add fixture corpus and regression metrics |

## Non-negotiable scrutiny rules

1. A passing unit test proves the tested behavior, not an adjacent claim.
2. A mathematical identity proves the identity, not a physical interpretation built on top of it.
3. A Git commit proves repository history, not scientific truth.
4. A cryptographic attestation proves provenance/integrity of the attested artifact, not the usefulness or correctness of the artifact.
5. Extraordinary performance claims require an explicit baseline and raw measurements.
6. Independent verification requires a party/environment other than the originating execution path.
7. If a claim cannot be operationalized, it remains theoretical or symbolic rather than being silently promoted.

## Verification target

The goal of the Hyperblog/Hyperbolic Time Chamber is therefore not to manufacture PASS labels. It is to drive every claim toward one of three defensible endpoints:

- **VERIFIED** by reproducible evidence;
- **REFUTED** by a failed test;
- **THEORETICAL/DOCUMENTED** with the missing evidence explicitly named.
