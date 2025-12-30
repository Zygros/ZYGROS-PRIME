# AIOX_ABI - Cartridge Interface Specification
# Generated: 2025-10-13T17:55:06Z
# CHRONOS ID: CHRONOS-20251013175506

## Purpose
A minimal, signed ABI for AIOX cartridges (modular capability units).

## Lifecycle Functions (all must be implemented)
- `init(config: JSON) -> { "status":"ok"|"error","meta":{} }`
- `step(input: JSON) -> { "output":JSON,"side_effects":[],"audit":{} }`
- `audit() -> { "health": "...", "consumed_keys": [], "last_run": "ISO" }`
- `shutdown() -> { "status":"shutdown" }`

## Security Constraints
- Cartridges run in sandboxed containers with limited syscalls.
- Network access requires an intent packet signed by Demiurge.
- Cartridges must declare dependencies and resource limits.

## Manifest (cartridge.json)
Each cartridge includes:
```
{
  "name": "string",
  "version": "semver",
  "author": "string",
  "hash": "<sha256>",
  "entry": "module:callable",
  "abi": "AIOX_ABI_v1",
  "permissions": ["read:knowledge","write:ledger","call:external-api"],
  "signature": "<signature>"
}
```

## Auditing & Telemetry
- Cartridges emit structured audit events to `/ledger` with CHRONOS references.
- Failed audits auto-disable the cartridge until human review.

---
