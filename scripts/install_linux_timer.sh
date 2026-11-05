#!/usr/bin/env bash
# Install a user-level systemd timer for LOCAL-ONLY swing research.
# Requires an explicitly configured, chmod-600 credential file outside git.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="$REPO/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Create venv first: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi
CONF="$HOME/.config/stock-research"
CREDS="$CONF/alpaca.env"
if [[ ! -f "$CREDS" ]]; then
  echo "Missing credentials: $CREDS" >&2
  echo "Create a chmod-600 file with ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY for approved personal market data access." >&2
  exit 1
fi
if [[ "$(stat -c %a "$CREDS")" != "600" ]]; then
  echo "Credential file must have chmod 600: $CREDS" >&2
  exit 1
fi
mkdir -p "$HOME/.config/systemd/user"
SERVICE="$HOME/.config/systemd/user/stock-research-private.service"
TIMER="$HOME/.config/systemd/user/stock-research-private.timer"
cat > "$SERVICE" <<EOF
[Unit]
Description=Private EOD swing-research scenario (never trades)

[Service]
Type=oneshot
WorkingDirectory=$REPO
EnvironmentFile=$CREDS
ExecStart=$PY $REPO/private_trade_report.py --source alpaca --feed sip
PrivateTmp=true
NoNewPrivileges=true
UMask=0077
EOF
cat > "$TIMER" <<EOF
[Unit]
Description=Refresh personal swing research weekdays at 16:45 America/Chicago

[Timer]
OnCalendar=Mon..Fri *-*-* 16:45:00 America/Chicago
Persistent=true
Unit=stock-research-private.service

[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now stock-research-private.timer
echo "Installed a private weekday 4:45 PM Central timer."
echo "Verify with: systemctl --user list-timers stock-research-private.timer"
echo "Run once: systemctl --user start stock-research-private.service"
echo "Read the private report: $REPO/private_reports/latest.html"
echo "User timers normally require an active user session; enable linger separately if this host must run while logged off."
