"""Fetch population counts by subzone from Singapore Open Data API."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

import httpx
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "api_config.json"
RAW_POPULATION_DIR = ROOT_DIR / "data" / "raw" / "population"


def load_api_config() -> Dict[str, Any]:
    """Load API configuration from JSON file."""
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


API_CONFIG = load_api_config()


def fetch_population_data(target_date: Optional[str] = None, limit: int = 5000) -> Path:
    """Fetch population by subzone data and save it to the raw data directory.

    Args:
        target_date: Optional date string (YYYY-MM-DD) retained in metadata for lineage.
        limit: Maximum number of records to request from the API.

    Returns:
        The path to the saved JSON file containing metadata and payload.
    """
    try:
        RAW_POPULATION_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_suffix = f"_{target_date}" if target_date else "_latest"
        output_file = RAW_POPULATION_DIR / f"population_by_subzone{date_suffix}_{timestamp}.json"

        population_config = API_CONFIG["nea"]["population_by_subzone"]
        dataset_id = population_config["dataset_id"]
        base_url = population_config["base_url"]
        url = f"{base_url}={dataset_id}"

        params: Dict[str, Any] = {"limit": limit}
        if target_date:
            params["filters"] = json.dumps({"year": target_date})
            print(f"Fetching population data filtered by year/date: {target_date}")
        else:
            print("Fetching latest population by subzone data...")

        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            population_payload = response.json()

        records = population_payload.get("result", {}).get("records", [])
        metadata = {
            "fetch_timestamp": timestamp,
            "target_date": target_date,
            "api_endpoint": url,
            "parameters": params,
            "record_count": len(records),
        }

        output_data = {
            "metadata": metadata,
            "data": population_payload,
        }

        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"Population data saved to: {output_file}")
        print(f"Records fetched: {metadata['record_count']}")

        df = pd.DataFrame(records)
        print("\nPopulation Data Preview:")
        if df.empty:
            print("No records returned from the API.")
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
    fetch_population_data()