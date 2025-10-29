"""Utilities for downloading and previewing URA subzone boundary polygons.

This module orchestrates a two-step call to Singapore's Data.gov.sg polling
API to retrieve Master Plan 2019 subzone geometries and save them into the raw
data lake. The saved artifact always contains the raw GeoJSON response together
with provenance metadata so downstream processing pipelines can reason about
source, timestamp, and applied filters.

Usage:
    >>> from scripts.acquisition.load_subzone_bounds import fetch_subzone_boundaries
    >>> fetch_subzone_boundaries()
    PosixPath('.../data/raw/boundaries/subzone_boundaries_latest_<timestamp>.json')

All functions prefer explicit helpers (for configuration, requests, metadata
assembly, and previews) to keep cyclomatic complexity low while preserving the
existing behaviour of the acquisition routine.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

import httpx
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "api_config.json"
RAW_BOUNDARIES_DIR = ROOT_DIR / "data" / "raw" / "boundaries"


def load_api_config() -> Dict[str, Any]:
    """Load the API configuration JSON.

    Returns:
        Dict[str, Any]: Parsed configuration dictionary containing dataset IDs
            and base URLs for all NEA endpoints.
    """
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
'''
https://data.gov.sg/datasets/d_8594ae9ff96d0c708bc2af633048edfb/view
           },
        "subzone_boundaries": {
            "dataset_id": "d_4fbb5f1c-3b4e-4a2f-8c1d-2d0e9f3b2a5c",
            "base_url": "https://api-open.data.gov.sg/v1/public/api/datasets",
            "description": "URA Master Plan 2019 subzone boundary polygons"
        }
          
dataset_id = "d_8594ae9ff96d0c708bc2af633048edfb"
url = "https://api-open.data.gov.sg/v1/public/api/datasets/" + dataset_id + "/poll-download"
        
response = requests.get(url)
json_data = response.json()
if json_data['code'] != 0:
    print(json_data['errMsg'])
    exit(1)

url = json_data['data']['url']
response = requests.get(url)
print(response.text)

'''

API_CONFIG = load_api_config()


def fetch_subzone_boundaries(target_date: Optional[str] = None) -> Path:
    """Fetch subzone boundary GeoJSON and persist it as a raw artifact.

    Args:
        target_date (Optional[str]): Specific polling date (``YYYY-MM-DD``). The
            underlying endpoint ignores this parameter today but we retain it for
            future-proofing and to record provenance metadata.

    Returns:
        Path: Location of the saved JSON file containing metadata and GeoJSON payload.
    """
    try:
        _ensure_output_directory()

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        poll_url = _poll_endpoint()
        output_path = _output_path(target_date, timestamp)

        print(f"Fetching subzone boundaries for date: {target_date or 'latest'}")

        with httpx.Client(timeout=30.0) as client:
            poll_payload = _request_poll_payload(client, poll_url)
            data_url = _extract_data_url(poll_payload)
            print(f"Data URL obtained: {data_url}")

            geojson_payload = _download_geojson(client, data_url)

        features = _extract_features(geojson_payload)
        metadata = _compose_metadata(timestamp, target_date, poll_url, data_url, len(features))
        _write_output(output_path, metadata, geojson_payload)

        _preview_features(features)
        return output_path

    except httpx.HTTPStatusError as e:
        print(f"Error code: {e.response.status_code}, HTTP Error: {e.response.text}")
        raise
    except httpx.TimeoutException:
        print("Error code: TIMEOUT, Connection timeout - API server not responding")
        raise
    except json.JSONDecodeError as e:
        print(f"Error code: JSON_DECODE, Invalid JSON response: {str(e)}")
        raise
    except Exception as e:
        print(f"Error code: UNKNOWN, Unexpected error: {str(e)}")
        raise


def _ensure_output_directory() -> None:
    """Create the raw boundaries directory if it does not yet exist."""
    RAW_BOUNDARIES_DIR.mkdir(parents=True, exist_ok=True)


def _poll_endpoint() -> str:
    """Return the polling endpoint for the subzone boundary dataset."""
    config = API_CONFIG["nea"]["subzone_boundaries"]
    return f"{config['base_url']}/{config['dataset_id']}/poll-download"


def _output_path(target_date: Optional[str], timestamp: str) -> Path:
    """Build the output file path for a given date/timestamp combination."""
    suffix = f"_{target_date}" if target_date else "_latest"
    return RAW_BOUNDARIES_DIR / f"subzone_boundaries{suffix}_{timestamp}.json"


def _request_poll_payload(client: httpx.Client, url: str) -> Dict[str, Any]:
    """Request polling payload from Data.gov.sg and return the parsed JSON."""
    response = client.get(url)
    response.raise_for_status()
    return response.json()


def _extract_data_url(payload: Dict[str, Any]) -> str:
    """Extract the downloadable data URL from the polling payload.

    Raises:
        RuntimeError: If the API signals a non-zero "code" or lacks the expected
            ``data.url`` structure.
    """
    if payload.get("code") != 0:
        error_msg = payload.get("errMsg", "Unknown API error")
        print(f"Error code: {payload.get('code')}, API Error: {error_msg}")
        raise RuntimeError(f"API Error: {error_msg}")

    data = payload.get("data", {})
    if not isinstance(data, dict) or "url" not in data:
        raise RuntimeError("API response missing data.url field")
    return data["url"]


def _download_geojson(client: httpx.Client, url: str) -> Dict[str, Any]:
    """Download the GeoJSON payload from the provided data URL."""
    response = client.get(url)
    response.raise_for_status()
    return response.json()


def _extract_features(payload: Dict[str, Any]) -> list[Dict[str, Any]]:
    """Pull the feature collection out of the GeoJSON payload."""
    if not isinstance(payload, dict):
        return []
    return payload.get("features", []) or []


def _compose_metadata(timestamp: str, target_date: Optional[str], poll_url: str, data_url: str, record_count: int) -> Dict[str, Any]:
    """Assemble provenance metadata about the download."""
    return {
        "fetch_timestamp": timestamp,
        "target_date": target_date,
        "api_endpoint": poll_url,
        "data_url": data_url,
        "record_count": record_count,
    }


def _write_output(path: Path, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
    """Persist the combined metadata and payload as JSON."""
    output_data = {"metadata": metadata, "data": payload}
    path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Subzone boundary data saved to: {path}")
    print(f"Records fetched: {metadata['record_count']}")


def _preview_features(features: list[Dict[str, Any]]) -> None:
    """Print a lightweight preview of feature attributes for operator feedback."""
    # Flatten the "properties" dict of each feature to inspect key columns quickly.
    df = pd.DataFrame([feature.get("properties", {}) for feature in features])
    preview_columns = [
        col
        for col in ("SUBZONE_N", "PLN_AREA_N", "REGION_N", "CA_IND")
        if col in df.columns
    ]

    print("\nSubzone Boundary Data Preview:")
    if df.empty:
        print("No features returned from the API.")
        return

    if preview_columns:
        print(df[preview_columns].head())
        return

    print(df.head())


if __name__ == "__main__":
    fetch_subzone_boundaries()