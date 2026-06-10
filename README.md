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
    {
      "id": "A",
      "speaker": "other",
      "speech_act": "Greet the learner informally",
      "lines": [
        { "content": "Guten Morgen!", "context": "" },
        { "content": "Hallo, guten Morgen!", "context": "more casual" }
      ]
    },
    {
      "id": "B",
      "speaker": "learner",
      "speech_act": "Return the greeting",
      "text": "Guten Morgen!"
    },
    {
      "id": "C1",
      "speaker": "other",
      "speech_act": "Ask how the learner is doing",
      "after": "B",
      "lines": [
        { "content": "Wie geht's?", "context": "informal" },
        { "content": "Wie geht es Ihnen?", "context": "formal" }
      ]
    }
  ]
}
```

- Each utterance needs either `lines` (array of sentences with optional `context`) or `text` (single sentence shorthand, no context)
- `lines` and `text` populate both `DialogLine` records and `SituationalUtterance` records (so sentences are also available for standalone practice)
- `after` references the `id` of the preceding utterance(s); omit it for a linear sequence
- `after` can be an array (`["X", "Y"]`) to express convergence from multiple branches

## Visualize models

```bash
uv run manage.py graph_models core -o models.png
```
