# HTC∞ Minimal Formal Specification

## Core Entities
- Mutation
- Iteration
- Governor
- Checkpoint

## State Machine
PROPOSE → VALIDATE_SCOPE → EXPERIMENT → MEASURE → DECIDE → CHECKPOINT → COOLDOWN

## Decisions
- PROMOTE
- HOLD
- REJECT
- ROLLBACK

## Required Tables
### iterations
- id, timestamp, mutation_id, decision, rationale

### metrics
- iteration_id, metric, baseline, variant, delta, confidence

### archive
- checkpoint_hash, artifact_refs, chain_anchor

## Safety Governors
- Scope boundary enforcement
- Metric immutability per iteration
- Cooldown after rollback