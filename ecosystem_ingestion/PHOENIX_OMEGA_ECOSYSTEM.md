# 🐦‍🔥 PHOENIX Ω — Ecosystem Discovery & Capability Ingestion

Status: **ARCHITECTURAL INTEGRATION — additive, provenance-preserving**

Owner: Justin Conzet / Zygros

## Purpose

Create a governed ingestion boundary between the external AI ecosystem and Phoenix/ZYGROS-PRIME.

The engine discovers candidate capabilities from GitHub, Hugging Face, MCP, Spaces, papers, datasets, skills, and benchmarks. Discovery does **not** imply trust, execution, promotion, or authorship.

## Governing loop

```text
DISCOVER → EXTRACT → NORMALIZE → DEDUPLICATE → PROVENANCE
→ SANDBOX → BENCHMARK → ADVERSARIAL TEST → VERIFY
→ PROMOTE → REGISTER → COMPOSE → EVOLVE
```

## Evidence levels

- L0 — discovered/name only
- L1 — public documentation inspected
- L2 — source/artifact inspected
- L3 — reproducible execution
- L4 — tests/benchmark evidence
- L5 — independent verification

Promotion must never be inferred from L0/L1 alone.

## Capability manifest

```yaml
capability_id:
source_platform:
source_url:
repository:
revision:
artifact_type:
author:
license:
discovered_at:
interface:
inputs: []
outputs: []
dependencies: []
phoenix_layer:
compatibility:
security_risk:
sandbox_required: true
evidence_level: L0
benchmarks: []
provenance:
parent_capabilities: []
derived_capabilities: []
status: candidate
```

## Initial high-priority external research targets

The first discovery set includes recursive self-improvement, harness self-improvement, memory evolution, skill evolution, self-modifying agents, automated AI research, evolutionary coding, MCP/tool retrieval, and agent benchmarks.

Representative candidates discovered during the initial scan include:

- Arvid-pku/Godel_Agent
- keskival/recursive-self-improvement-suite
- leezythu/Awesome-Harness-Self-Improvement
- AlexWortega/OpenRsi
- zjunlp/LightRSI
- Gen-Verse/PAST-Bench

These are **candidate references**, not imported code and not promoted capabilities.

## Security boundary

External content is untrusted input. Never execute arbitrary fetched code merely because it was discovered. Installation, dependency resolution, credential access, network access, filesystem mutation, and promotion require explicit execution policy and verification.

## Append-only rule

New discoveries are appended to the registry. Existing records are not silently rewritten. Corrections preserve prior state and add a correction record with evidence.

## Research question

Can Phoenix continuously discover external computational capabilities, evaluate them experimentally, compose successful capabilities, and improve the mechanism by which discovery/evaluation occurs?

This is a research objective, not a claim of achieved AGI or autonomous recursive general intelligence.
