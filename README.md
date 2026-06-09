# siballe

## Setup

```bash
uv sync
```

## Run

```bash
uv run manage.py runserver
```

## Database

```bash
uv run manage.py migrate
uv run manage.py createsuperuser
```

## Visualize models

```bash
uv run manage.py graph_models core -o models.png
```
