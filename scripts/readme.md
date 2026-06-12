# Scripts

| Script | Purpose | Run command |
|--------|---------|-------------|
| data_ingestion.py | Load and inspect all 10 CSVs | `python scripts/data_ingestion.py` |
| live_nav_fetch.py | Fetch live NAV from mfapi.in | `python scripts/live_nav_fetch.py` |
| scheduled_nav_fetch.py | Bonus B1 — scheduled NAV fetch | `python scripts/scheduled_nav_fetch.py` |
| etl_pipeline.py | Load all data into SQLite | `python scripts/etl_pipeline.py` |
| compute_metrics.py | Compute all 7 performance metrics | `python scripts/compute_metrics.py` |
| recommender.py | Fund recommendation engine | `python scripts/recommender.py` |