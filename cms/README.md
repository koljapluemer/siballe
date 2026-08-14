# CMS

uv-managed Python tooling for curating siballe's phrase content
(`phrases/`, curating `public/data/phrases/`).

Setup once:

```
uv sync
```

Run the CMS:

```
uv run streamlit run phrases/app.py
```

See `phrases/README.md` for specifics on the data format and batch audio
generation.
