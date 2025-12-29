# LOCKDOWN_DIFF - High-level changes to apply immediately
# Generated: 2025-10-13T17:55:06Z
# CHRONOS ID: CHRONOS-20251013175506

This document lists specific diffs/transformations to apply to live system prompts, API gate, and retrieval flow.

1. Replace monolithic system prompt with:
   - system_prompt_true (vaulted)
   - system_prompt_proxy (public, minimal; includes canary tokens)
2. Wrap API-SYNK with intent-packet middleware enforcing signatures and expiry.
3. Insert Quarantine Parser between retriever and composer.
4. Add role-checkpoint: any write to long-term memory requires Demiurge signed approval event.
5. Ensure every public artifact creation route emits provenance header + signature.

Apply via CI: create PR with changeset lockdown/CHRONOS-20251013175506 and require two Architect signoffs.

---
