# Pull near-real-time weather observations for rainfall and temperature.
# CWQ - Supports date parameters for temporal lag analysis (2 months ago)

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import httpx
import json
from typing import Optional

RAW_WEATHER = Path(__file__).resolve().parents[2] / "data" / "raw" / "weather"

def fetch_air_temperature(date: Optional[str] = None) -> None:
    """Fetch air temperature data from Singapore Open Data API.
    
    Args:
        date: Date string in format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS (SGT)
              If None, fetches latest data
    """
    temp_dir = RAW_WEATHER / "temperature"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_suffix = f"_{date.replace('-', '').replace(':', '')}" if date else "_latest"
    output_file = temp_dir / f"air_temperature{date_suffix}_{timestamp}.json"
    
    url = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
    params = {"date": date} if date else {}
    
    print(f"Fetching air temperature data for: {date if date else 'latest'}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            temp_data = response.json()
        
        output_file.write_text(json.dumps(temp_data, indent=2), encoding="utf-8")
        print(f"Air temperature data saved to: {output_file}")
        
        # Validate data structure
        if "data" in temp_data and "readings" in temp_data["data"]:
            readings_count = len(temp_data["data"]["readings"])
            print(f"Retrieved {readings_count} temperature readings")
        else:
            print("Warning: Unexpected data structure in temperature response")
            
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching temperature data: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
        raise

def fetch_rainfall(date: Optional[str] = None) -> None:
    """Fetch rainfall data from Singapore Open Data API.
    
    Args:
        date: Date string in format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS (SGT)
              If None, fetches latest data
    """
    rainfall_dir = RAW_WEATHER / "rainfall"
    rainfall_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_suffix = f"_{date.replace('-', '').replace(':', '')}" if date else "_latest"
    output_file = rainfall_dir / f"rainfall{date_suffix}_{timestamp}.json"
    
    url = "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
    params = {"date": date} if date else {}
    
    print(f"Fetching rainfall data for: {date if date else 'latest'}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            rainfall_data = response.json()
        
        output_file.write_text(json.dumps(rainfall_data, indent=2), encoding="utf-8")
        print(f"Rainfall data saved to: {output_file}")
        
        # Validate data structure
        if "data" in rainfall_data and "readings" in rainfall_data["data"]:
            readings_count = len(rainfall_data["data"]["readings"])
            print(f"Retrieved {readings_count} rainfall readings")
        else:
            print("Warning: Unexpected data structure in rainfall response")
            
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching rainfall data: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"Error fetching rainfall data: {e}")
        raise

def get_lagged_date(months_ago: int = 2) -> str:
    """Calculate date from months ago for temporal lag analysis.
    
    Args:
        months_ago: Number of months to go back (default 2 for dengue lag)
        
    Returns:
        Date string in YYYY-MM-DD format
    """
    today = datetime.now()
    lagged_date = today - timedelta(days=months_ago * 30)  # Approximate months
    return lagged_date.strftime("%Y-%m-%d")

def fetch_weather(date: Optional[str] = None, use_temporal_lag: bool = False) -> None:
    """Fetch both air temperature and rainfall data.
    
    Args:
        date: Specific date to fetch (YYYY-MM-DD format)
        use_temporal_lag: If True, fetch data from 2 months ago
    """
    RAW_WEATHER.mkdir(parents=True, exist_ok=True)
    
    if use_temporal_lag and not date:
        date = get_lagged_date(2)
        print(f"Using temporal lag: fetching data from {date}")
    
    try:
        fetch_air_temperature(date)
        fetch_rainfall(date)
        print("Weather data collection completed successfully")
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        raise



if __name__ == "__main__":
    fetch_weather()
