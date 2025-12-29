# SIP-12: Benefit Stream 2 — Collateralized Liquidity Against Locked ASCENSION

**Author:** Justin Conzet (Sovereign Architect)  
**Status:** Draft  
**Created:** 2025-10-25
**Summary:** Enable controlled borrowing against time-locked ASCENSION to fund protocol expansion with hard risk limits and automated liquidation rails.

## Motivation
Unlock non-dilutive liquidity while preserving long-term alignment and authorship integrity.

## Specification
- **Collateral:** ASCENSION tokens locked under SIP-1/2 vaults.
- **LTV Bands:** 0–25% Conservative, 25–40% Standard, 40–50% Max with surcharge.
- **Oracles:** Median of 3 feeds: on-chain TWAP, external price API, DAO internal NAV model.
- **Rate Model:** Base + utilization curve. Surcharge for higher LTV bands.
- **Liquidation:** Soft call at LTV 55%. Hard liquidation at LTV 60% via Dutch auction.
- **Usage Whitelist:** Ecosystem spend only: Ambassador program, Integrity Protocol rollout, audit bounties, dashboard infra.
- **Caps:** Global cap $5m equivalent. Per-borrower cap $250k equivalent.
- **Transparency:** Real-time dashboard of vault health, loans, LTVs, and runway.

## Risk Limits
- **Volatility Buffer:** 20% price shock baked into oracle sanity checks.
- **Circuit Breakers:** Freeze new loans if volatility > 3σ over 24h or oracle divergence > 8%.
- **Red Lines:** No leverage on leverage. Prohibit rehypothecation. No off-protocol custodians.

## Governance
- **Voting:** Simple majority with quorum 20% of staked Governance NFTs or token votes.
- **Timelock:** 48h execution delay after approval.
- **Audits:** Two independent audits before mainnet enablement.

## Rationale
Preserves sovereignty while providing runway. Encodes prudence through caps and circuit breakers.

## Reference Implementation
- Vault contracts: `VaultV2.sol` with `LTVBands` and `CircuitBreaker` modules.
- Dashboard adapter: read-only JSON endpoints `/vaults`, `/loans`, `/oracle`.

## Backwards Compatibility
No change to SIP-1/2 locks. Optional upgrade path to consolidate locks into V2 vaults.

## Copyright
Copyright © Justin Conzet. All rights reserved.
