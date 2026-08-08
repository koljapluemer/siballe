set dotenv-load

# Auto-detect any Chrome/Chromium-family browser on this machine so flutter's
# `-d chrome` device works without hand-editing a path per dev machine.
# Respects a manually-set CHROME_EXECUTABLE (e.g. via .env) if present.
_detected_chrome := `command -v google-chrome google-chrome-stable chromium chromium-browser microsoft-edge microsoft-edge-stable 2>/dev/null | head -n1`
export CHROME_EXECUTABLE := env("CHROME_EXECUTABLE", _detected_chrome)

# Run the backend (migrating first) and the Flutter frontend together.
# Ctrl+C stops the frontend and kills the backgrounded backend server.
dev:
    #!/usr/bin/env bash
    set -euo pipefail
    (cd backend && uv run manage.py migrate)
    (cd backend && uv run manage.py runserver) &
    backend_pid=$!
    trap "kill $backend_pid 2>/dev/null" EXIT
    cd frontend && flutter run -d chrome --web-port=5000 --dart-define=API_BASE_URL=http://localhost:8000/api

migrate:
    cd backend && uv run manage.py migrate

makemigrations:
    cd backend && uv run manage.py makemigrations

# Load/refresh the bootstrap sample data (safe to re-run).
loaddata:
    cd backend && uv run manage.py load_bootstrap_data

test:
    cd backend && uv run manage.py test

# Run the Flutter app against a locally running backend.
frontend:
    cd frontend && flutter run -d chrome --web-port=5000 --dart-define=API_BASE_URL=http://localhost:8000/api
