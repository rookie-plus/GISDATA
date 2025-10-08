# Pull near-real-time weather observations for rainfall and temperature.
# CWQ
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import httpx
import json
from typing import Optional

RAW_WEATHER = Path(__file__).resolve().parents[2] / "data" / "raw" / "weather"

def fetch_air_temperature(target_date: Optional[str] = None) -> None:
    """
    Fetch air temperature data from Singapore Open Data API.
    
    Args:
        target_date: Optional date string in YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format.
                    If None, fetches latest data.
                    For temporal lag analysis, use date from 2 months ago.
    """
    try:
        temp_dir = RAW_WEATHER / "temperature"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_suffix = f"_{target_date}" if target_date else "_latest"
        output_file = temp_dir / f"air_temperature{date_suffix}_{timestamp}.json"
        
        url = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
        
        # Add date parameter if specified
        params = {}
        if target_date:
            params['date'] = target_date
            print(f"Fetching air temperature data for date: {target_date}")
        else:
            print("Fetching latest air temperature data...")
        
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            temp_data = response.json()
            
            # Add metadata for processing pipeline
            metadata = {
                "fetch_timestamp": timestamp,
                "target_date": target_date,
                "api_endpoint": url,
                "station_count": len(temp_data.get('data', {}).get('stations', [])) if isinstance(temp_data, dict) else 0
            }
            
            # Combine data with metadata
            output_data = {
                "metadata": metadata,
                "data": temp_data
            }
        
        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"Air temperature data saved to: {output_file}")
        print(f"Weather stations: {metadata['station_count']}")

    except httpx.HTTPStatusError as e:
        print(f"Error code: {e.response.status_code}, HTTP Error: {e.response.text}")
        print(f"Failed to fetch temperature data - HTTP {e.response.status_code}")
        if e.response.status_code == 404:
            print("Tip: Weather data might not be available for the requested date")
        raise
    except httpx.TimeoutException:
        print("Error code: TIMEOUT, Connection timeout - API server not responding")
        print("Failed to fetch temperature data - Connection timeout")
        raise
    except json.JSONDecodeError as e:
        print(f"Error code: JSON_DECODE, Invalid JSON response: {str(e)}")
        print("Failed to parse temperature data - Invalid JSON response")
        raise
    except Exception as e:
        print(f"Error code: UNKNOWN, Unexpected error: {str(e)}")
        print(f"Unexpected error in temperature data acquisition: {type(e).__name__}")
        raise

def fetch_rainfall(target_date: Optional[str] = None) -> None:
    """
    Fetch rainfall data from Singapore Open Data API.
    
    Args:
        target_date: Optional date string in YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format.
                    If None, fetches latest data.
                    For temporal lag analysis, use date from 2 months ago.
    """
    try:
        rainfall_dir = RAW_WEATHER / "rainfall"
        rainfall_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_suffix = f"_{target_date}" if target_date else "_latest"
        output_file = rainfall_dir / f"rainfall{date_suffix}_{timestamp}.json"
        
        url = "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
        
        # Add date parameter if specified
        params = {}
        if target_date:
            params['date'] = target_date
            print(f"Fetching rainfall data for date: {target_date}")
        else:
            print("Fetching latest rainfall data...")
        
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            rainfall_data = response.json()
            
            # Add metadata for processing pipeline
            metadata = {
                "fetch_timestamp": timestamp,
                "target_date": target_date,
                "api_endpoint": url,
                "station_count": len(rainfall_data.get('data', {}).get('stations', [])) if isinstance(rainfall_data, dict) else 0
            }
            
            # Combine data with metadata
            output_data = {
                "metadata": metadata,
                "data": rainfall_data
            }
        
        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"Rainfall data saved to: {output_file}")
        print(f"Weather stations: {metadata['station_count']}")

    except httpx.HTTPStatusError as e:
        print(f"Error code: {e.response.status_code}, HTTP Error: {e.response.text}")
        print(f"Failed to fetch rainfall data - HTTP {e.response.status_code}")
        if e.response.status_code == 404:
            print("Tip: Rainfall data might not be available for the requested date")
        raise
    except httpx.TimeoutException:
        print("Error code: TIMEOUT, Connection timeout - API server not responding")
        print("Failed to fetch rainfall data - Connection timeout")
        raise
    except json.JSONDecodeError as e:
        print(f"Error code: JSON_DECODE, Invalid JSON response: {str(e)}")
        print("Failed to parse rainfall data - Invalid JSON response")
        raise
    except Exception as e:
        print(f"Error code: UNKNOWN, Unexpected error: {str(e)}")
        print(f"Unexpected error in rainfall data acquisition: {type(e).__name__}")
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
