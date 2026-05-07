#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_BIN="$ROOT_DIR/flask_ENV/bin"
FLASK_BIN="$VENV_BIN/flask"
PYTHON_BIN="$VENV_BIN/python"
APP_URL="http://127.0.0.1:8080"
SERVER_LOG="$ROOT_DIR/.server.log"
REQUEST_DIR="$ROOT_DIR/RequestTests"
STARTED_SERVER=0

cleanup() {
    if [[ "$STARTED_SERVER" -eq 1 ]] && [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

if [[ ! -x "$FLASK_BIN" || ! -x "$PYTHON_BIN" ]]; then
    echo "Virtual environment tools not found in flask_ENV/bin."
    echo "Create/restore the venv first, then re-run this script."
    exit 1
fi

if [[ ! -d "$REQUEST_DIR" ]]; then
    echo "Request test folder not found: $REQUEST_DIR"
    exit 1
fi

cd "$ROOT_DIR"
export FLASK_APP=demo_app

if [[ ! -e "$ROOT_DIR/instance/demo_app.sqlite" ]]; then
    "$FLASK_BIN" init-db
fi

if lsof -ti tcp:8080 >/dev/null 2>&1; then
    if ! curl -s "$APP_URL" >/dev/null; then
        echo "Port 8080 is in use but API is not reachable at $APP_URL"
        exit 1
    fi
    echo "Using already running server on $APP_URL"
else
    "$FLASK_BIN" run --host 127.0.0.1 --port 8080 >"$SERVER_LOG" 2>&1 &
    SERVER_PID=$!
    STARTED_SERVER=1

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
fi

scripts=(
    "createUsers.py"
    "tokenGeneration.py"
    "retrieveUsers.py"
    "retrieveUser.py"
    "updateUser.py"
)

for script in "${scripts[@]}"; do
    echo "===== Running $script ====="
    "$PYTHON_BIN" "$REQUEST_DIR/$script"
    echo
 done

echo "All request tests completed successfully."
