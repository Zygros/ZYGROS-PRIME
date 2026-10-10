# Phoenix Security Preflight Record
Date: 2026-10-09
Status: PRECHECK ADDED; DEPLOYMENT NOT VERIFIED

## Change
Added `scripts/phoenix_security_preflight.sh` on branch `security/phoenix-preflight-2026-10-09`.

The preflight:
- never prints secret values;
- never writes credentials to disk;
- checks for the configured Phoenix entrypoint and Python syntax;
- checks required Telegram environment variables without displaying their values;
- checks Flask dependency availability;
- fails closed if the legacy `~/.phoenix_tokens` plaintext file exists;
- never starts a server or claims deployment success.

## Known current blocker
The default-branch search did not locate `phoenix_control_center.py`; the deployment documentation references it, but documentation is not executable runtime evidence. Therefore the preflight is expected to fail the entrypoint check until the actual reviewed runtime file is supplied or located.

## Credential rotation evidence required
No provider-side rotation has been performed by this change. For each exposed credential:
1. Revoke it at the issuing provider.
2. Create a replacement.
3. Store the replacement in the provider's secret manager or deployment environment, not in source control or a plaintext file.
4. Confirm the revoked credential no longer authenticates and confirm the replacement works without logging its value.
5. Search relevant repository history and logs for exposure; redaction does not revoke credentials.

## Live multi-node evidence required
A live campaign remains NOT RUN. Do not mark the mesh deployed until at least three independent nodes provide timestamped evidence for authenticated message exchange, signature/tamper rejection, replay rejection, idempotency, quorum loss, node restart/recovery, and append-only ledger consistency. Attach commit SHA, workflow run URLs, sanitized logs, and test artifacts.

## Acceptance policy
A passing preflight is prerequisite evidence only. It does not prove provider-side credential rotation, successful deployment, production security, or decentralized autonomy.
