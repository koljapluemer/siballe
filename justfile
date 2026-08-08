set dotenv-load

# Run the backend dev server (migrating first).
dev:
    cd backend && uv run manage.py migrate && uv run manage.py runserver

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
    cd frontend && flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000/api
