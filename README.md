# siballe

A language-learning app built around a graph of interconnected content — vocab and
sentences (`Node`s) linked by relationships like translation, part-of, and example
(`Rel`s) — surfaced to learners through `Situation`s (e.g. "buying something in the
bakery") they're interested in.

## Architecture

- **`backend/`** — Django + Django REST Framework, managed with `uv`. A single app
  (`learning`) holds the domain model (`Node`, `Rel`, `Situation`, `SituationRelation`)
  and two read endpoints: listing situations, and generating a random flashcard
  exercise for a situation by walking the graph. JWT auth (`djangorestframework-simplejwt`)
  and a custom `AUTH_USER_MODEL` are wired up from the start, though the current MVP
  endpoints are open (`AllowAny`) since the frontend has no login screen yet.
- **`frontend/`** — Flutter (web + Android, iOS later), a simple three-tab app
  (Learn / Add / Situations) that talks to the backend over HTTP.

No learning progress is persisted yet — this is an MVP for the content-graph model and
the exercise-generation logic, not a spaced-repetition system.

## Running it

Backend (from repo root):

```sh
just dev        # migrate + runserver, http://localhost:8000
just loaddata   # load bootstrap sample data (fra "Smalltalk in French")
just test
```

First time setup: copy `backend/.env.example` to `backend/.env` and adjust as needed
(defaults to a local sqlite DB, no Postgres required for dev).

Frontend:

```sh
just frontend   # flutter run -d chrome, pointed at the local backend
```

Or run Flutter yourself with `flutter run --dart-define=API_BASE_URL=<backend-url>/api`
(on the Android emulator, use `http://10.0.2.2:8000/api` instead of `localhost`).

## Deploying

The backend is set up for a standard Ubuntu VPS deploy: Postgres via `DATABASE_URL`,
static files via Whitenoise (`manage.py collectstatic`), and `gunicorn
config.wsgi:application` as the WSGI entrypoint. Set `DJANGO_DEBUG=False` and configure
`DJANGO_ALLOWED_HOSTS`/`DJANGO_CORS_ALLOWED_ORIGINS` via environment variables in
production — see `backend/.env.example`.
