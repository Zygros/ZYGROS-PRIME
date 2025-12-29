# PROVENANCE_SPEC for Sovereign Knowledge Compilation System
# Generated: 2025-10-13T17:55:06Z
# CHRONOS ID: CHRONOS-20251013175506

## Goal
Ensure every artifact (documents, code, generated assets, API responses) carries verifiable origin metadata.

## Immutable Header (auto-appended)
Each sealed artifact MUST include the following header (plaintext + machine-parsable JSON block):

```
--- BEGIN SOVEREIGN HEADER ---
Author: Justin Conzet
System: Sovereign Knowledge Compilation System (SKCS)
Artifact-Type: <document|code|model-output|asset>
Timestamp: 2025-10-13T17:55:06Z
CHRONOS-ID: CHRONOS-20251013175506
SHA256: <hex>
Lineage: <CHRONOS-ID(s) or file refs>
Signature: <detached-signature>
--- END SOVEREIGN HEADER ---
```

## Signing & Verification
- Use an Architect private key (RSA/ECDSA in HSM) to sign SHA256 digests.
- Provide a public verifier script (`verify_provenance.py`) that:
  - recomputes SHA256
  - verifies signature
  - checks CHRONOS ledger entry matches artifact metadata

## SPDX-style License Block
- Each artifact includes a short SPDX identifier and a usage policy reference (policy ID + version + CHRONOS hash).

## Lineage & Replayability
- Build artifacts must include `Build-Recipe` pointer (BUILD_RECIPE_SCHEMA.json ID).
- Replaying a Build-Recipe should deterministically reproduce the artifact given the same input corpus and model versions.

## Public Verifiability
- Publish public-key fingerprints on a stable anchor (website / DID / DNS TXT).
- Keep a public read-only CHRONOS mirror for transparency (no secrets).

---
