# Real-Time Dengue Map

This workspace hosts a streaming dengue risk dashboard for GE5219.

## Key folders
- `data/` — data lake for raw, processed, and aggregated assets
- `scripts/` — ingestion, processing, and analysis pipelines
- `visualization/` — H5 front-end assets for the live map
- `config/` — API keys, app tuning, and connection metadata
- `models/` — analytic weights and saved model artefacts

## Getting started
1. just run ```docs/A_Real_Time_Dengue_Map.ipynb```

> or

1. Populate `config/api_config.json` with real credentials.
2. Install dependencies via `pip install -r dependencies.txt`.
3. Run `python main.py` to start the development server.
4. Point a browser at `http://localhost:8000` to view the dashboard.

## References


1. National Environment Agency. (2020). Dengue Clusters (GEOJSON) (2025) [Dataset]. data.gov.sg. Retrieved October 8, 2025 from https://data.gov.sg/datasets/d_dbfabf16158d1b0e1c420627c0819168/view
