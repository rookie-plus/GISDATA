"""Fetch subzone boundary GeoJSON data via Singapore Open Data polling endpoint."""
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
    """Load API configuration from JSON file."""
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


API_CONFIG = load_api_config()


def fetch_subzone_boundaries(target_date: Optional[str] = None) -> Path:
    """Fetch subzone boundary GeoJSON and persist it with metadata.

    Args:
        target_date: Optional date string (YYYY-MM-DD) captured in metadata for provenance.

    Returns:
        The path to the saved JSON file containing metadata and GeoJSON payload.
    """
    try:
        RAW_BOUNDARIES_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_suffix = f"_{target_date}" if target_date else "_latest"
        output_file = RAW_BOUNDARIES_DIR / f"subzone_boundaries{date_suffix}_{timestamp}.json"

        boundary_config = API_CONFIG["nea"]["subzone_boundaries"]
        dataset_id = boundary_config["dataset_id"]
        base_url = boundary_config["base_url"]
        poll_url = f"{base_url}/{dataset_id}/poll-download"

        print(f"Fetching subzone boundaries for date: {target_date or 'latest'}")

        with httpx.Client(timeout=30.0) as client:
            poll_response = client.get(poll_url)
            poll_response.raise_for_status()
            poll_payload = poll_response.json()

            if poll_payload.get("code") != 0:
                error_msg = poll_payload.get("errMsg", "Unknown API error")
                print(f"Error code: {poll_payload.get('code')}, API Error: {error_msg}")
                raise RuntimeError(f"API Error: {error_msg}")

            data_url = poll_payload["data"]["url"]
            print(f"Data URL obtained: {data_url}")

            data_response = client.get(data_url)
            data_response.raise_for_status()
            geojson_payload = data_response.json()

        features = []
        if isinstance(geojson_payload, dict):
            features = geojson_payload.get("features", [])

        metadata = {
            "fetch_timestamp": timestamp,
            "target_date": target_date,
            "api_endpoint": poll_url,
            "data_url": data_url,
            "record_count": len(features),
        }

        output_data = {
            "metadata": metadata,
            "data": geojson_payload,
        }

        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"Subzone boundary data saved to: {output_file}")
        print(f"Records fetched: {metadata['record_count']}")

        df = pd.DataFrame([feature.get("properties", {}) for feature in features])
        preview_columns = [col for col in ("SUBZONE_N", "PLN_AREA_N", "REGION_N", "CA_IND") if col in df.columns]

        print("\nSubzone Boundary Data Preview:")
        if df.empty:
            print("No features returned from the API.")
        elif preview_columns:
            print(df[preview_columns].head())
        else:
            print(df.head())

        return output_file

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


if __name__ == "__main__":
    fetch_subzone_boundaries()