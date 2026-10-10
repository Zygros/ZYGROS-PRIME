#!/usr/bin/env bash
# Phoenix runtime security preflight.
# Fail closed: this script never prints secrets, persists tokens, or launches a server.
set -Eeuo pipefail
umask 077

ROOT="${PHOENIX_ROOT:-$PWD}"
ENTRYPOINT="${PHOENIX_ENTRYPOINT:-$ROOT/phoenix_control_center.py}"
failures=0

pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; failures=$((failures + 1)); }

printf '%s\n' 'PHOENIX SECURITY PREFLIGHT' 'Mode: validation only; no network listener will be started.'
printf 'Working root: %s\n' "$ROOT"

if [[ -d "$ROOT" ]]; then pass 'runtime root exists'; else fail 'runtime root does not exist'; fi
if [[ -f "$ENTRYPOINT" ]]; then
  pass 'Phoenix entrypoint exists'
  if python -m py_compile "$ENTRYPOINT"; then pass 'entrypoint compiles'; else fail 'entrypoint compilation failed'; fi
else
  fail "Phoenix entrypoint not found at configured path"
fi

for name in TELEGRAM_TOKEN_CONTROL TELEGRAM_TOKEN_EXPERIMENTAL CHAT_ID; do
  if [[ -n "${!name:-}" ]]; then
    pass "$name is set (value intentionally hidden)"
  else
    fail "$name is missing from the process environment"
  fi
done

if python - <<'PY'
import importlib.util
missing = [name for name in ("flask", "flask_socketio") if importlib.util.find_spec(name) is None]
if missing:
    print("Missing Python modules: " + ", ".join(missing))
    raise SystemExit(1)
print("Required Flask modules are available.")
PY
then pass 'Python runtime dependencies are importable'; else fail 'required Python runtime dependencies are unavailable'; fi

if [[ -e "$HOME/.phoenix_tokens" ]]; then
  fail 'legacy plaintext token file exists; migrate credentials to a secret manager or process environment, then securely remove the legacy copy after confirming rotation'
else
  pass 'legacy plaintext token file not present'
fi

if (( failures > 0 )); then
  printf 'PREFLIGHT FAILED: %d check(s) require remediation. No runtime launched.\n' "$failures" >&2
  exit 1
fi

printf '%s\n' 'PREFLIGHT PASSED: prerequisites are present. This does not prove deployment health or multi-node autonomy.'
