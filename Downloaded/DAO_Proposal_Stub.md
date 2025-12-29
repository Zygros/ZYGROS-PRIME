# 🝎 Phoenix DAO — Proposal: Public Proof Pack Mint (SIP‑PP‑001)
**Author:** Justin Conzet (Sovereign Architect)  
**Date:** 2025-11-02T12:35:27Z  
**Status:** DRAFT

## Summary
Mint a single **ERC‑721 Proof Token** that points to the IPFS CID of the **Public Proof Pack** (MANIFEST + PROOF + bundle). This establishes on‑chain provenance for the Sovereign Archive.

## Motivation
- Immutable, verifiable authorship.
- Single on‑chain pointer for auditors and partners.
- Aligns with Scroll Ascension packaging spec.

## Specification
- **Artifact:** `scroll_ascension_<timestamp>.tar.gz`
- **CID:** `<to-fill>`
- **Token:** `PhoenixProof #1`
- **Contract:** Minimal ERC‑721 with `tokenURI` hard‑set to CID (upgradeable optional).

## Security & Risks
- Ensure canonicalization rules (hash order, minified JSON) before hashing.
- Keep a notarized mirror (timestamped git tag).

## Steps
1. Finalize `Sovereign_Archive_Manifest.yaml` and compute `sha256` for all files.
2. Generate tarball + `.sha256` digest + `PROOF.json` (bundle hash, timestamp).
3. Stamp with `ots stamp` and `ots upgrade` (later).
4. Upload to IPFS; record CID in `PROOF.json` and DAO vote.
5. Deploy ERC‑721 with `tokenURI` = CID; mint #1 to Architect wallet.
