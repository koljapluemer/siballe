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

## Import dialogs

Dialogs can be authored as JSON files and imported with:

```bash
uv run manage.py import_dialog dialogs/my_dialog.json
# or multiple files at once
uv run manage.py import_dialog dialogs/*.json
```

Each file is one dialog. The `Language` (by `iso3`) must exist in the database first. `Situation` and `SpeechAct` are created automatically if not found. Already-imported dialogs (matched by name + situation) are skipped.

**File format** (`dialogs/example.json`):

```json
{
  "situation": "Greeting a colleague at the office",
  "language": "deu",
  "name": "Morning greeting – formal",
  "learner_role": "new employee",
  "other_role": "senior colleague",
  "utterances": [
    { "id": "A", "speaker": "other",   "speech_act": "Greet the learner informally" },
    { "id": "B", "speaker": "learner", "speech_act": "Return the greeting" },
    { "id": "C1", "speaker": "other",  "speech_act": "Ask how the learner is doing", "after": "B" },
    { "id": "C2", "speaker": "other",  "speech_act": "Invite the learner for coffee", "after": "B" }
  ]
}
```

- `after` references the `id` of the preceding utterance(s); omit it for a linear sequence
- `after` can be an array (`["X", "Y"]`) to express convergence from multiple branches

## Visualize models

```bash
uv run manage.py graph_models core -o models.png
```
