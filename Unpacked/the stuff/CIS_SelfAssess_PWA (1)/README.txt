# CIS Self‑Assess PWA (phone‑first)

This is a one‑tap app that asks the CIS Kernel to self‑assess **until it reaches ≥97%**.

## Use
1) Open `index.html` in your mobile browser (or host these files anywhere).
2) Set the **Kernel URL** (default `http://localhost:8011`).
3) Tap **Self‑Assess to Target**.

## Tips
- The kernel comes from your `cis_kernel_v0_2.zip` and exposes:
  - `POST /self_assess/until?min_score=97&max_rounds=5`
  - `POST /self_assess/once`
  - `GET  /self_assess/status`
- App installs as a PWA and works offline for UI assets.
