"""
Scaffold the GE5219 real-time dengue mapping project structure.

Run this script from the `GE5219-Dengue` folder. It's idempotent: it will only
create folders/files that are missing so you can safely re-run it after manual
modifications. Empty directories receive a `.gitkeep` so they are versioned.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, List


ROOT = Path(__file__).resolve().parent


def write_text_if_missing(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def ensure_dir(path: Path) -> bool:
    if path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return False
    path.mkdir(parents=True, exist_ok=True)
    return True


def ensure_gitkeep_if_empty(dir_path: Path) -> bool:
    dir_path.mkdir(parents=True, exist_ok=True)
    entries = [p for p in dir_path.iterdir() if p.name != ".gitkeep"]
    if entries:
        return False
    gitkeep = dir_path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")
        return True
    return False


def main() -> int:
    files: Dict[str, str] = {
        "README.md": (
            "# Real-Time Dengue Map\n\n"
            "This workspace hosts a streaming dengue risk dashboard for GE5219.\n\n"
            "## Key folders\n"
            "- `data/` — data lake for raw, processed, and aggregated assets\n"
            "- `scripts/` — ingestion, processing, and analysis pipelines\n"
            "- `visualization/` — H5 front-end assets for the live map\n"
            "- `config/` — API keys, app tuning, and connection metadata\n"
            "- `models/` — analytic weights and saved model artefacts\n\n"
            "## Getting started\n"
            "1. Populate `config/api_config.json` with real credentials.\n"
            "2. Install dependencies via `pip install -r dependencies.txt`.\n"
            "3. Run `python main.py` to start the development server.\n"
            "4. Point a browser at `http://localhost:8000` to view the dashboard.\n"
        ),
        ".gitignore": (
            "# Data caches\n"
            "data/raw/**\n"
            "data/processed/**\n"
            "data/aggregated/**\n"
            "logs/**\n"
            "*.pyc\n"
            "__pycache__/\n"
            "env/\n"
            ".env\n"
        ),
        "requirements.md": (
            "# System Requirements\n\n"
            "- Python 3.11+\n"
            "- Node.js 18+ (for front-end tooling)\n"
            "- GDAL 3.x with Python bindings\n"
            "- PostgreSQL + PostGIS (optional, for spatial persistence)\n"
            "- Access to NEA dengue API and weather endpoints\n"
        ),
        "dependencies.txt": (
            "fastapi==0.115.0\n"
            "uvicorn[standard]==0.30.0\n"
            "httpx==0.27.0\n"
            "pandas==2.2.2\n"
            "geopandas==0.14.4\n"
            "rasterio==1.3.10\n"
            "shapely==2.0.4\n"
            "scikit-learn==1.5.1\n"
            "pyproj==3.6.1\n"
            "jinja2==3.1.4\n"
        ),
        "main.py": (
            "#!/usr/bin/env python3\n\n"
            "# Minimal FastAPI application bootstrap for the dengue dashboard.\n\n"
            "from fastapi import FastAPI\n"
            "from fastapi.staticfiles import StaticFiles\n"
            "from pathlib import Path\n"
            "from typing import Dict\n\n"
            "APP = FastAPI(title=\"GE5219 Real-Time Dengue Map\")\n\n"
            "static_root = Path(__file__).parent / \"visualization\" / \"static\"\n"
            "APP.mount(\"/static\", StaticFiles(directory=static_root), name=\"static\")\n\n"
            "@APP.get(\"/health\")\n"
            "async def healthcheck() -> Dict[str, str]:\n"
            "    return {\"status\": \"ok\"}\n\n"
            "@APP.get(\"/\")\n"
            "async def index() -> Dict[str, str]:\n"
            "    return {\"message\": \"Serve visualization from /static/templates/index.html\"}\n\n"
            "if __name__ == \"__main__\":\n"
            "    import uvicorn\n\n"
            "    uvicorn.run(APP, host=\"0.0.0.0\", port=8000, reload=True)\n"
        ),
        "config/api_config.json": json.dumps(
            {
                "nea": {
                    "base_url": "https://api.data.gov.sg/v1/environment/dengue-clusters",
                    "api_key": "",
                },
                "weather": {
                    "base_url": "https://api.data.gov.sg/v1/environment",
                    "api_key": "",
                },
                "satellite": {
                    "provider": "",  # e.g. SentinelHub, Planet
                    "api_key": "",
                },
            },
            indent=2,
        )
        + "\n",
        "config/app_config.json": json.dumps(
            {
                "refresh_interval_minutes": 5,
                "spatial_reference": "EPSG:3414",
                "frontend": {
                    "websocket_url": "ws://localhost:8000/ws/live",
                    "default_basemap": "CartoDB.Positron",
                },
                "processing": {
                    "ndvi_threshold": 0.3,
                    "population_density_bins": [1000, 3000, 6000],
                },
            },
            indent=2,
        )
        + "\n",
        "scripts/acquisition/fetch_dengue.py": (
            "# Fetch dengue cluster data from NEA endpoints and save to RAW storage.\n\n"
            "from __future__ import annotations\n\n"
            "from datetime import datetime\n"
            "from pathlib import Path\n"
            "import httpx\n"
            "import json\n\n"
            "RAW_DIR = Path(__file__).resolve().parents[2] / \"data\" / \"raw\" / \"dengue\"\n\n"
            "def fetch_clusters() -> None:\n"
            "    RAW_DIR.mkdir(parents=True, exist_ok=True)\n"
            "    timestamp = datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")\n"
            "    output_file = RAW_DIR / f\"clusters_{timestamp}.json\"\n"
            "    with httpx.Client(timeout=30.0) as client:\n"
            "        response = client.get(\"https://api.data.gov.sg/v1/environment/dengue-clusters\")\n"
            "        response.raise_for_status()\n"
            "    output_file.write_text(json.dumps(response.json(), indent=2), encoding=\"utf-8\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    fetch_clusters()\n"
        ),
        "scripts/acquisition/fetch_weather.py": (
            "# Pull near-real-time weather observations for rainfall and temperature.\n\n"
            "from __future__ import annotations\n\n"
            "from datetime import datetime\n"
            "from pathlib import Path\n"
            "import httpx\n"
            "import json\n\n"
            "RAW_WEATHER = Path(__file__).resolve().parents[2] / \"data\" / \"raw\" / \"weather\"\n\n"
            "def fetch_weather() -> None:\n"
            "    RAW_WEATHER.mkdir(parents=True, exist_ok=True)\n"
            "    timestamp = datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")\n"
            "    output_file = RAW_WEATHER / f\"weather_{timestamp}.json\"\n"
            "    with httpx.Client(timeout=30.0) as client:\n"
            "        response = client.get(\"https://api.data.gov.sg/v1/environment/air-temperature\")\n"
            "        response.raise_for_status()\n"
            "    output_file.write_text(json.dumps(response.json(), indent=2), encoding=\"utf-8\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    fetch_weather()\n"
        ),
        "scripts/acquisition/fetch_satellite.py": (
            "# Placeholder for syncing satellite imagery for NDVI derivation.\n\n"
            "from pathlib import Path\n\n"
            "SAT_DIR = Path(__file__).resolve().parents[2] / \"data\" / \"raw\" / \"satellite\"\n\n"
            "def sync_satellite_imagery() -> None:\n"
            "    SAT_DIR.mkdir(parents=True, exist_ok=True)\n"
            "    # TODO: integrate with SentinelHub/PlanetStage APIs\n"
            "    print(\"Satellite imagery sync placeholder\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    sync_satellite_imagery()\n"
        ),
        "scripts/processing/create_ndvi.py": (
            "# Convert calibrated satellite imagery into NDVI rasters.\n\n"
            "def build_ndvi_stack():\n"
            "    raise NotImplementedError(\"Implement NDVI processing pipeline\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    build_ndvi_stack()\n"
        ),
        "scripts/processing/calculate_population_density.py": (
            "# Compute population density surfaces per subzone.\n\n"
            "def main():\n"
            "    raise NotImplementedError(\"Implement population density workflow\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    main()\n"
        ),
        "scripts/processing/apply_temporal_lag.py": (
            "# Generate lagged weather features for dengue forecasting.\n\n"
            "def main():\n"
            "    raise NotImplementedError(\"Implement temporal lag routine\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    main()\n"
        ),
        "scripts/processing/interpolate_surfaces.py": (
            "# Spatially interpolate dengue risk surfaces over the study area.\n\n"
            "def main():\n"
            "    raise NotImplementedError(\"Implement interpolation logic\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    main()\n"
        ),
        "scripts/analysis/ahp_model.py": (
            "# Analytic Hierarchy Process (AHP) weighting model for dengue risk.\n\n"
            "def run_ahp():\n"
            "    raise NotImplementedError(\"Implement AHP weighting\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    run_ahp()\n"
        ),
        "scripts/analysis/risk_score_calculator.py": (
            "# Combine hazard, exposure, and vulnerability layers into a risk score.\n\n"
            "def calculate_scores():\n"
            "    raise NotImplementedError(\"Implement dengue risk scoring\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    calculate_scores()\n"
        ),
        "visualization/templates/index.html": (
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "  <head>\n"
            "    <meta charset=\"UTF-8\" />\n"
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
            "    <title>GE5219 Real-Time Dengue Map</title>\n"
            "    <link rel=\"stylesheet\" href=\"/static/css/style.css\" />\n"
            "  </head>\n"
            "  <body>\n"
            "    <div id=\"app\">Loading dengue map…</div>\n"
            "    <script src=\"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js\"></script>\n"
            "    <script src=\"/static/js/live.js\"></script>\n"
            "  </body>\n"
            "</html>\n"
        ),
        "visualization/app.js": (
            "import L from 'leaflet';\n\n"
            "export function initMap() {\n"
            "  const map = L.map('app').setView([1.3521, 103.8198], 12);\n"
            "  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {\n"
            "    maxZoom: 19,\n"
            "    attribution: '&copy; OpenStreetMap contributors',\n"
            "  }).addTo(map);\n"
            "  return map;\n"
            "}\n"
        ),
        "visualization/static/css/style.css": (
            "html, body {\n"
            "  margin: 0;\n"
            "  padding: 0;\n"
            "  height: 100%;\n"
            "  font-family: 'Segoe UI', sans-serif;\n"
            "}\n\n"
            "#app {\n"
            "  height: 100vh;\n"
            "}\n"
        ),
        "visualization/static/js/live.js": (
            "import { initMap } from '../../app.js';\n\n"
            "const map = initMap();\n\n"
            "async function refreshClusters() {\n"
            "  try {\n"
            "    const response = await fetch('/api/dengue/latest');\n"
            "    if (!response.ok) {\n"
            "      throw new Error(`Request failed: ${response.status}`);\n"
            "    }\n"
            "    const geojson = await response.json();\n"
            "    // TODO: Visualise clusters\n"
            "    console.debug('Fetched clusters', geojson);\n"
            "  } catch (error) {\n"
            "    console.error('Cluster refresh error', error);\n"
            "  }\n"
            "}\n\n"
            "refreshClusters();\n"
            "setInterval(refreshClusters, 5 * 60 * 1000);\n"
        ),
    }

    empty_dirs: List[str] = [
        "data/raw/dengue",
        "data/raw/weather/rainfall",
        "data/raw/weather/temperature",
        "data/raw/boundaries",
        "data/raw/population",
        "data/raw/satellite",
        "data/processed/dengue",
        "data/processed/weather/current",
        "data/processed/weather/lagged",
        "data/processed/ndvi",
        "data/processed/population_density",
        "data/aggregated",
        "models/ahp_weights",
        "visualization/static/images",
        "logs",
        "tests",
        "docs",
    ]

    created_dirs: List[str] = []
    created_files: List[str] = []
    skipped_files: List[str] = []
    created_gitkeeps: List[str] = []

    for rel_path in files.keys():
        parent = (ROOT / rel_path).parent
        if ensure_dir(parent):
            created_dirs.append(parent.relative_to(ROOT).as_posix())

    for d in empty_dirs:
        p = ROOT / d
        if ensure_dir(p):
            created_dirs.append(p.relative_to(ROOT).as_posix())

    for rel_path, content in files.items():
        p = ROOT / rel_path
        if write_text_if_missing(p, content):
            created_files.append(rel_path)
        else:
            skipped_files.append(rel_path)

    for d in empty_dirs:
        p = ROOT / d
        if ensure_gitkeep_if_empty(p):
            created_gitkeeps.append((p / ".gitkeep").relative_to(ROOT).as_posix())

    print("Dengue map project structure ensured at:", ROOT)
    print(f"- Directories created: {len(created_dirs)}")
    print(f"- Files created: {len(created_files)} (skipped existing: {len(skipped_files)})")
    print(f"- .gitkeep files added: {len(created_gitkeeps)}")

    if created_dirs:
        print("\nNew directories:")
        for d in sorted(set(created_dirs)):
            print(f"  - {d}")

    if created_files:
        print("\nNew files:")
        for f in sorted(created_files):
            print(f"  - {f}")

    if created_gitkeeps:
        print("\nNew .gitkeep files:")
        for g in sorted(created_gitkeeps):
            print(f"  - {g}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
