#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load SSH_SERVER from .env
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    source "$SCRIPT_DIR/.env"
else
    echo "Error: .env file not found. Create one with SSH_SERVER=user@host" >&2
    exit 1
fi

if [[ -z "${SSH_SERVER:-}" ]]; then
    echo "Error: SSH_SERVER not set in .env" >&2
    exit 1
fi

REMOTE_DIR="~/noteweaver"
SERVICE_NAME="noteweaver-server"

echo "==> Copying noteweaver to $SSH_SERVER:$REMOTE_DIR"
ssh "$SSH_SERVER" "mkdir -p $REMOTE_DIR"
rsync -avz --exclude '.venv' --exclude '__pycache__' --exclude '.env' --exclude '*.pyc' --exclude 'noteweaver_queue.db' --exclude 'tmp' --exclude '*.log' --exclude '.git' "$SCRIPT_DIR/" "$SSH_SERVER:$REMOTE_DIR/"

echo "==> Installing with uv"
ssh "$SSH_SERVER" "source ~/.profile && cd $REMOTE_DIR && uv sync"

echo "==> Setting up systemd user service"
ssh "$SSH_SERVER" bash -s <<REMOTE_SCRIPT
set -euo pipefail
source "\$HOME/.profile" 2>/dev/null || true

REMOTE_DIR="\$HOME/noteweaver"
SERVICE_FILE="\$HOME/.config/systemd/user/${SERVICE_NAME}.service"
UV_PATH="\$(which uv)"

mkdir -p "\$HOME/.config/systemd/user"

echo "==> Creating service unit"
cat > "\$SERVICE_FILE" <<EOF
[Unit]
Description=NoteWeaver Server
After=network.target

[Service]
Type=simple
WorkingDirectory=\$REMOTE_DIR
ExecStart=\$REMOTE_DIR/.venv/bin/python -m noteweaver.server.app
Environment="HOME=\$HOME"
Environment="PATH=\$REMOTE_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable ${SERVICE_NAME}

if systemctl --user is-active --quiet ${SERVICE_NAME}; then
    echo "==> Restarting service"
    systemctl --user restart ${SERVICE_NAME}
else
    echo "==> Starting service"
    systemctl --user start ${SERVICE_NAME}
fi

echo "==> Service status:"
systemctl --user status ${SERVICE_NAME} --no-pager
REMOTE_SCRIPT

echo "==> Done!"
