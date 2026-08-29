# Zygros Quality Gate

This repository participates in the Zygros federation quality standard.

## Promotion requirements
- Reproducible tests must pass before promotion.
- Security and dependency checks must pass.
- Claims must carry an evidence status: DESIGNED, IMPLEMENTED, TESTED, BENCHMARKED, VERIFIED, or HISTORICAL.
- Autonomous changes must be isolated, reviewable, and reversible.
- Secrets and credentials must never be committed.
- Production capability must not be inferred from source presence alone.

## Improvement loop
OBSERVE -> DIAGNOSE -> PROPOSE -> TEST -> SECURITY CHECK -> REGRESSION CHECK -> SCORE -> PROMOTE/REJECT -> LEDGER.

A 10/10 score is earned by current reproducible evidence; it is never assigned by declaration.