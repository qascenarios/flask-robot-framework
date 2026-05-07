#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_BIN="$ROOT_DIR/flask_ENV/bin"
FLASK_BIN="$VENV_BIN/flask"
ROBOT_BIN="$VENV_BIN/robot"
APP_URL="http://127.0.0.1:8080"
SERVER_LOG="$ROOT_DIR/.server.log"

cleanup() {
    if [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

if [[ ! -x "$FLASK_BIN" || ! -x "$ROBOT_BIN" ]]; then
    echo "Virtual environment tools not found in flask_ENV/bin."
    echo "Create/restore the venv first, then re-run this script."
    exit 1
fi

cd "$ROOT_DIR"
export FLASK_APP=demo_app

if [[ ! -e "$ROOT_DIR/instance/demo_app.sqlite" ]]; then
    "$FLASK_BIN" init-db
fi

if lsof -ti tcp:8080 >/dev/null 2>&1; then
    echo "Port 8080 is already in use. Stop that process, then run ./run_tests.sh"
    exit 1
fi

"$FLASK_BIN" run --host 127.0.0.1 --port 8080 >"$SERVER_LOG" 2>&1 &
SERVER_PID=$!

for _ in {1..30}; do
    if curl -s "$APP_URL" >/dev/null; then
        break
    fi
    sleep 1
done

if ! curl -s "$APP_URL" >/dev/null; then
    echo "Server did not start successfully."
    echo "Server log:"
    cat "$SERVER_LOG"
    exit 1
fi

"$ROBOT_BIN" RobotTest/ "$@"
