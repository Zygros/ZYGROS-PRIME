# Zygros Autonomous Engineering Agent

This package provides a guarded autonomous improvement loop for the Zygros ecosystem.

## Loop

`inspect → test → measure → learn → propose → isolate → test → promote`

The current implementation performs inspection, testing, scoring, bounded policy learning, and an append-only improvement log. It intentionally does **not** modify source code autonomously by default.

## Federated scope

`config.json` records the repositories that form the current Zygros federation. The runtime can use that manifest as the inventory boundary when a separate sync/checkout layer is available.

## Safety gates

- `auto_apply` defaults to `false`.
- Protected paths include secrets, `.env`, GitHub workflows, and `.git`.
- Candidate changes must be tested before promotion.
- Change size and minimum score are configurable.
- State and observations are retained for auditability.

## Run

```bash
python -m zygros_autonomy.agent
```

Set `ZYGROS_GOAL` to change the engineering objective.

## Important distinction

"Self-improving" here means measurable adaptation of the agent's policy and iterative proposal/evaluation—not unrestricted self-modification. That boundary is deliberate: autonomous code changes should be reversible, tested, and attributable.
