"""Fetch population counts by subzone from Singapore Open Data API."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

import httpx


ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "api_config.json"
RAW_POPULATION_DIR = ROOT_DIR / "data" / "raw" / "population"


def _load_api_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


API_CONFIG = _load_api_config()


def _population_settings() -> Dict[str, str]:
    return API_CONFIG["nea"]["population_by_subzone"]


def _prepare_output_path(target_date: Optional[str], timestamp: str) -> Path:
    suffix = f"_{target_date}" if target_date else "_latest"
    return RAW_POPULATION_DIR / f"population_by_subzone{suffix}_{timestamp}.json"


def _build_request_params(target_date: Optional[str], limit: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": limit}
    if target_date:
        params["filters"] = json.dumps({"year": target_date})
    return params


def _log_request(target_date: Optional[str]) -> None:
    if target_date:
        print(f"Fetching population data for year: {target_date}")
    else:
        print("Fetching latest population by subzone data...")


def _request_population_payload(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        print(f"Error code: {status}, HTTP Error: {exc.response.text}")
        raise
    except httpx.TimeoutException:
        print("Error code: TIMEOUT, Connection timeout - API server not responding")
        raise
    except json.JSONDecodeError as exc:
        print(f"Error code: JSON_DECODE, Invalid JSON response: {exc}")
        raise
    except Exception as exc:
        print(f"Error code: UNKNOWN, Unexpected error: {exc}")
        raise


def _extract_records(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("result", {}).get("records", []) if isinstance(payload, dict) else []


def _compile_metadata(timestamp: str, target_date: Optional[str], url: str, params: Dict[str, Any], record_count: int) -> Dict[str, Any]:
    return {
        "fetch_timestamp": timestamp,
        "target_date": target_date,
        "api_endpoint": url,
        "parameters": params,
        "record_count": record_count,
    }


def _write_raw_output(path: Path, payload: Dict[str, Any], metadata: Dict[str, Any]) -> None:
    RAW_POPULATION_DIR.mkdir(parents=True, exist_ok=True)
    output_data = {"metadata": metadata, "data": payload}
    path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")


def fetch_population_data(target_date: Optional[str] = None, limit: int = 5000) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    settings = _population_settings()
    url = f"{settings['base_url']}={settings['dataset_id']}"
    params = _build_request_params(target_date, limit)

    _log_request(target_date)
    payload = _request_population_payload(url, params)
    records = _extract_records(payload)

    metadata = _compile_metadata(timestamp, target_date, url, params, len(records))
    output_path = _prepare_output_path(target_date, timestamp)
    _write_raw_output(output_path, payload, metadata)

    print(f"Population data saved to: {output_path}")
    print(f"Records fetched: {len(records)}")
    return output_path


# Preview raw data only - NO processing
if __name__ == "__main__":
    result_path = fetch_population_data()
    try:
        # Simple preview of raw data structure
        import pandas as pd
        if str(result_path).endswith('.geojson'):
            import geopandas as gpd
            df = gpd.read_file(result_path)
        else:
            with open(result_path) as f:
                import json
                data = json.load(f)
                df = pd.DataFrame(data['data']['result']['records']
                     if 'result' in data['data'] else data['data']['features'])
        print("\nRaw Data Preview (first 5 rows):")
        print(df.head())
    except Exception as e:
        print(f"Preview error: {e}")