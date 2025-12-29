# Android / One UI Quick Optimize (No Root)

## 0) Safety/Backup
- Backup to cloud or PC first. Enable Google Drive/Photos **or** use `rclone` and `vault_backup_sync.sh`.

## 1) Developer Options
Settings → About phone → Software information → tap *Build number* 7x → back → Developer options:
- Window/Transition/Animator scale → **0.5x** (or **Off** if you like snappy)
- Background process limit → **Standard** (only change to 3/4 if you NEED it)
- Disable HW overlays → **On** (optional, helps UI smoothness)
- Force peak refresh rate (if present) → **On**
- USB debugging → **On** (for ADB)
- Wi‑Fi scan throttling → **On**
- Mobile data always active → **Off**

## 2) Battery & Performance
- Settings → Battery → **Adaptive battery On**, **Background usage limits**: put junk into **Sleeping** or **Deep sleeping**.
- Turn off **Nearby device scanning** if not used.
- Disable **Auto sync** for accounts you don’t use.

## 3) Privacy / Network
- Settings → Connections → **Private DNS**: `1dot1dot1dot1.cloudflare-dns.com` or `dns.google`.
- Use **NetGuard** / **RethinkDNS**. Default deny; allow only what you trust.

## 4) Home/UX
- Use a light launcher (Niagara / Nova). Remove Samsung Free: long‑press home → Settings → turn off.
- Reduce live wallpapers/widgets. Keep 1‑2 pages max.

## 5) Camera/Audio
- Try a GCam port for your A16 variant (MGC builds). If none stable, lock to Samsung camera at HDR On.
- Install **Wavelet** to EQ headphones; use *AutoEq* profiles.

## 6) Storage Hygiene
- Files by Google → remove junk.
- Move media to SD card; keep apps on internal.
- Run `dedupe_scan.py` monthly to archive duplicates.
