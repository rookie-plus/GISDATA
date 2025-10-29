# Pull near-real-time weather observations for rainfall and temperature.
# CWQ
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import httpx
import json

RAW_WEATHER = Path(__file__).resolve().parents[2] / "data" / "raw" / "weather"

_WEATHER_DATASETS: Dict[str, Dict[str, str]] = {
    "temperature": {
        "directory": "temperature",
        "prefix": "air_temperature",
        "endpoint": "https://api-open.data.gov.sg/v2/real-time/api/air-temperature",
        "display": "air temperature",
        "saved_label": "Air temperature",
        "failure_label": "temperature",
        "tip": "Tip: Weather data might not be available for the requested date",
        "parse_label": "temperature",
    },
    "rainfall": {
        "directory": "rainfall",
        "prefix": "rainfall",
        "endpoint": "https://api-open.data.gov.sg/v2/real-time/api/rainfall",
        "display": "rainfall",
        "saved_label": "Rainfall",
        "failure_label": "rainfall",
        "tip": "Tip: Rainfall data might not be available for the requested date",
        "parse_label": "rainfall",
    },
}


def fetch_air_temperature(target_date: Optional[str] = None) -> None:
    """Fetch air temperature data from Singapore's real-time API."""
    config = _WEATHER_DATASETS["temperature"]
    try:
        output_path, station_count = _fetch_weather_dataset(config, target_date)
        print(f"{config['saved_label']} data saved to: {output_path}")
        print(f"Weather stations: {station_count}")

    except httpx.HTTPStatusError as error:
        _handle_http_error(config, error)
        raise
    except httpx.TimeoutException:
        _handle_timeout(config)
        raise
    except json.JSONDecodeError as error:
        _handle_json_error(config, error)
        raise
    except Exception as error:
        _handle_generic_error(config, error)
        raise


def fetch_rainfall(target_date: Optional[str] = None) -> None:
    """Fetch rainfall data from Singapore's real-time API."""
    config = _WEATHER_DATASETS["rainfall"]
    try:
        output_path, station_count = _fetch_weather_dataset(config, target_date)
        print(f"{config['saved_label']} data saved to: {output_path}")
        print(f"Weather stations: {station_count}")

    except httpx.HTTPStatusError as error:
        _handle_http_error(config, error)
        raise
    except httpx.TimeoutException:
        _handle_timeout(config)
        raise
    except json.JSONDecodeError as error:
        _handle_json_error(config, error)
        raise
    except Exception as error:
        _handle_generic_error(config, error)
        raise

def fetch_weather(target_date: Optional[str] = None) -> None:
    """
    Fetch both air temperature and rainfall data.
    
    Args:
        target_date: Optional date string for temporal lag analysis.
                    Format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
    """
    try:
        RAW_WEATHER.mkdir(parents=True, exist_ok=True)
        
        print("=== Weather Data Acquisition ===")
        if target_date:
            print(f"Target date: {target_date} (for temporal lag analysis)")
        else:
            print("Fetching latest weather data...")
        
        fetch_air_temperature(target_date)
        fetch_rainfall(target_date)

        print("Weather data collection completed successfully")
        
    except Exception as e:
        print(f"Error in weather data acquisition: {e}")
        raise

def fetch_historical_weather(months_back: int = 2) -> None:
    """
    Fetch weather data from N months ago for temporal lag analysis.
    Based on research design: "rainfall lagging 2 months" and 
    "(lowest) air temperature lagging 2 months provided a better fitting model"
    
    Args:
        months_back: Number of months to go back (default: 2 for temporal lag)
    """
    target_date = (datetime.now() - timedelta(days=months_back * 30)).strftime("%Y-%m-%d")
    print(f"Fetching historical weather data from {months_back} months ago: {target_date}")
    print("Research note: 2-month lag provides better fitting model for dengue prediction")
    fetch_weather(target_date)



if __name__ == "__main__":
    # Example usage:
    # fetch_weather()  # Latest data
    # fetch_weather("2024-08-09")  # Specific date
    # fetch_historical_weather(2)  # 2 months ago for temporal lag
    
    print("=== Weather Data Acquisition ===")
    print("Fetching latest weather data...")
    fetch_weather()
    
    print("\nFetching historical weather data for temporal lag analysis...")
    fetch_historical_weather(2)
    
    print("\nWeather data acquisition completed!")


"""
API Documentation Notes:
- Air Temperature: Updated every minute from NEA weather stations (°C)
- Rainfall: Updated every 5 minutes from NEA weather stations (mm)
- Date format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS (SGT)
- Research finding: 2-month temporal lag provides better model fit
"""


def _fetch_weather_dataset(config: Dict[str, str], target_date: Optional[str]) -> Tuple[Path, int]:
    """Execute the full fetch-write cycle for a given weather dataset."""
    directory = RAW_WEATHER / config["directory"]
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output_path = _build_output_path(directory, config["prefix"], target_date, timestamp)

    params = _build_query_params(target_date)
    _log_request(config["display"], target_date)

    payload = _request_weather_payload(config["endpoint"], params)
    station_count = _extract_station_count(payload)

    metadata = _compose_metadata(timestamp, target_date, config["endpoint"], station_count)
    _write_payload(output_path, metadata, payload)
    return output_path, station_count


def _build_output_path(directory: Path, prefix: str, target_date: Optional[str], timestamp: str) -> Path:
    """Construct the output filepath using the dataset-specific naming scheme."""
    suffix = f"_{target_date}" if target_date else "_latest"
    return directory / f"{prefix}{suffix}_{timestamp}.json"


def _build_query_params(target_date: Optional[str]) -> Dict[str, str]:
    """Include the optional date parameter if an explicit target was provided."""
    if not target_date:
        return {}
    return {"date": target_date}


def _log_request(display_label: str, target_date: Optional[str]) -> None:
    """Emit a consistent status message before calling the external API."""
    if target_date:
        print(f"Fetching {display_label} data for date: {target_date}")
        return
    print(f"Fetching latest {display_label} data...")


def _request_weather_payload(endpoint: str, params: Dict[str, str]) -> Dict[str, Any]:
    """Perform the HTTP request and return the JSON payload."""
    with httpx.Client(timeout=30.0) as client:
        response = client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()


def _extract_station_count(payload: Dict[str, Any]) -> int:
    """Count stations for operator insight; guards against malformed payloads."""
    if not isinstance(payload, dict):
        return 0
    data = payload.get("data", {})
    if not isinstance(data, dict):
        return 0
    stations = data.get("stations", [])
    return len(stations) if isinstance(stations, list) else 0


def _compose_metadata(timestamp: str, target_date: Optional[str], endpoint: str, station_count: int) -> Dict[str, Any]:
    """Prepare metadata envelope stored alongside the raw payload."""
    return {
        "fetch_timestamp": timestamp,
        "target_date": target_date,
        "api_endpoint": endpoint,
        "station_count": station_count,
    }


def _write_payload(path: Path, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
    """Persist metadata and payload to disk as indented JSON."""
    output = {"metadata": metadata, "data": payload}
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")


def _handle_http_error(config: Dict[str, str], error: httpx.HTTPStatusError) -> None:
    """Mirror original HTTP error messaging for backwards compatibility."""
    status = error.response.status_code
    print(f"Error code: {status}, HTTP Error: {error.response.text}")
    print(f"Failed to fetch {config['failure_label']} data - HTTP {status}")
    if status == 404:
        print(config["tip"])


def _handle_timeout(config: Dict[str, str]) -> None:
    """Emit the original timeout guidance for operators."""
    print("Error code: TIMEOUT, Connection timeout - API server not responding")
    print(f"Failed to fetch {config['failure_label']} data - Connection timeout")


def _handle_json_error(config: Dict[str, str], error: json.JSONDecodeError) -> None:
    """Log JSON parsing failures with dataset-specific context."""
    print(f"Error code: JSON_DECODE, Invalid JSON response: {error}")
    print(f"Failed to parse {config['parse_label']} data - Invalid JSON response")


def _handle_generic_error(config: Dict[str, str], error: Exception) -> None:
    """Fallback handler to keep messaging consistent with legacy behaviour."""
    print(f"Error code: UNKNOWN, Unexpected error: {error}")
    print(f"Unexpected error in {config['failure_label']} data acquisition: {type(error).__name__}")
