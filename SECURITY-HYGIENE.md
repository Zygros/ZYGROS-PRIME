# Security Hygiene

This repository contains research, experiments, archives, and executable material. Security hygiene is part of the repository quality baseline.

## Credential rule

Never commit API keys, access tokens, private keys, session cookies, shell history, `.env` files, or copied credential-bearing command transcripts.

Use environment variables or a platform secret store instead. Before publishing or sharing a repository, inspect the complete working tree for credential material.

## Incident response

If a credential is ever committed:

1. Revoke or rotate it immediately at the issuing provider.
2. Remove the credential-bearing file from the current tree.
3. Search the repository history for prior exposure.
4. If the secret existed in Git history, rewrite the affected history using an approved local Git history-rewrite process and force-update the repository only after coordinating the change.
5. Re-run secret scanning after rotation and history cleanup.
6. Record the incident without reproducing the secret value.

Removing a file from the latest commit does **not** remove its contents from earlier Git commits.

## Evidence boundary

A green CI run is not a security certification. Repository claims should distinguish implemented, tested, benchmarked, verified, designed, and historical material.

## Safe reporting

When documenting an exposure, identify the file, commit, credential type, remediation status, and rotation status. Never paste the credential itself into an issue, README, commit message, or report.
