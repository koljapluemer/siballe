set dotenv-load

# Run the backend (migrating first) and the Vue frontend together.
# Ctrl+C stops the frontend and kills the backgrounded backend server.
dev:
    #!/usr/bin/env bash
    set -euo pipefail
    (cd backend && uv run manage.py migrate)
    (cd backend && uv run manage.py runserver) &
    backend_pid=$!
    trap "kill $backend_pid 2>/dev/null" EXIT
    cd vue && npm run dev

migrate:
    cd backend && uv run manage.py migrate

makemigrations:
    cd backend && uv run manage.py makemigrations

# Load/refresh the bootstrap sample data (safe to re-run).
loaddata:
    cd backend && uv run manage.py load_bootstrap_data

test:
    cd backend && uv run manage.py test

# Run the Vue app against a locally running backend.
frontend:
    cd vue && npm run dev

# --- Production deploy (see DEPLOY.md). `host` is an alias from your ~/.ssh/config. ---

# Build the Vue frontend bundle for production (run locally before deploying).
build-frontend-prod api_base_url:
    cd vue && VITE_API_BASE_URL={{api_base_url}} npm run build

# Sync the built frontend to the VPS (run after build-frontend-prod).
sync-frontend-prod host:
    rsync -avz --delete vue/dist/ {{host}}:/opt/siballe/frontend-web/

# Pull latest code, install deps, migrate, collectstatic, restart gunicorn on the VPS.
deploy-backend host:
    ssh {{host}} 'cd /opt/siballe/app && git pull --ff-only && cd backend && uv sync --frozen && uv run manage.py migrate --noinput && uv run manage.py collectstatic --noinput && sudo systemctl restart gunicorn-siballe'

# Full deploy: backend then frontend. Usage: just deploy siballe-vps http://VPS_IP/api
deploy host api_base_url: (deploy-backend host) (build-frontend-prod api_base_url) (sync-frontend-prod host)
