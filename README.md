# DumpCheck

Tennessee RV dump stations that are actually open, each checked against an official source and dated.

Static HTML built by `build.py` into `docs/`, served by GitHub Pages. Yeha, an AI research agent, verifies and adds stations on a schedule; its manual is `yeha/YEHA.md`.

```bash
pip install -r requirements.txt
python3 build.py --base-path "" --site-url http://localhost:8003   # local preview
python3 -m http.server 8003 -d docs
python3 build.py && python3 tools/check.py                         # before committing
```

Stations live in `data/stations.json`; guides in `content/guides/`.
