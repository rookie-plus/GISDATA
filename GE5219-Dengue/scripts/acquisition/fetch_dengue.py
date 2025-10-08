# Fetch dengue cluster data from NEA endpoints and save to RAW storage.
# CWQ

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import httpx
import json
from typing import Optional

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "dengue"

def fetch_clusters(target_date: Optional[str] = None) -> None:
    """
    Fetch dengue cluster data from Singapore Open Data API.
    
    Args:
        target_date: Optional date string in YYYY-MM-DD format.
                    If None, fetches latest data.
                    For temporal lag analysis, use date from 2 months ago.
    """
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        
        # Add date suffix to filename if specific date requested
        date_suffix = f"_{target_date}" if target_date else "_latest"
        output_file = RAW_DIR / f"dengue_clusters{date_suffix}_{timestamp}.json"

        # Singapore Open Data API endpoint for dengue clusters
        dataset_id = "d_dbfabf16158d1b0e1c420627c0819168"
        url = f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"
        
        print(f"Fetching dengue cluster data for date: {target_date or 'latest'}")
        
        with httpx.Client(timeout=30.0) as client:
            # First, get the download URL
            response = client.get(url)
            response.raise_for_status()
            
            api_response = response.json()
            if api_response.get('code') != 0:
                error_msg = api_response.get('errMsg', 'Unknown API error')
                print(f"Error code: {api_response.get('code')}, API Error: {error_msg}")
                raise RuntimeError(f"API Error: {error_msg}")
            
            # Get the actual data URL
            data_url = api_response['data']['url']
            print(f"Data URL obtained: {data_url}")
            
            # Fetch the actual dengue data
            data_response = client.get(data_url)
            data_response.raise_for_status()
            
            # Parse and save the data
            dengue_data = data_response.json()
            
            # Add metadata for processing pipeline
            metadata = {
                "fetch_timestamp": timestamp,
                "target_date": target_date,
                "api_endpoint": url,
                "data_url": data_url,
                "record_count": len(dengue_data.get('features', [])) if isinstance(dengue_data, dict) else len(dengue_data) if isinstance(dengue_data, list) else 0
            }
            
            # Combine data with metadata
            output_data = {
                "metadata": metadata,
                "data": dengue_data
            }
        
        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"Dengue cluster data saved to: {output_file}")
        print(f"Records fetched: {metadata['record_count']}")
        
    except httpx.HTTPStatusError as e:
        print(f"Error code: {e.response.status_code}, HTTP Error: {e.response.text}")
        print(f"Failed to fetch dengue data - HTTP {e.response.status_code}")
        raise
    except httpx.TimeoutException:
        print("Error code: TIMEOUT, Connection timeout - API server not responding")
        print("Failed to fetch dengue data - Connection timeout")
        raise
    except json.JSONDecodeError as e:
        print(f"Error code: JSON_DECODE, Invalid JSON response: {str(e)}")
        print("Failed to parse dengue data - Invalid JSON response")
        raise
    except Exception as e:
        print(f"Error code: UNKNOWN, Unexpected error: {str(e)}")
        print(f"Unexpected error in dengue data acquisition: {type(e).__name__}")
        raise

def fetch_historical_dengue(months_back: int = 2) -> None:
    """
    Fetch dengue data from N months ago for temporal lag analysis.
    
    Args:
        months_back: Number of months to go back (default: 2 for temporal lag)
    """
    target_date = (datetime.now() - timedelta(days=months_back * 30)).strftime("%Y-%m-%d")
    print(f"Fetching historical dengue data from {months_back} months ago: {target_date}")
    fetch_clusters(target_date)

if __name__ == "__main__":
    # Example usage:
    # fetch_clusters()  # Latest data
    # fetch_clusters("2024-08-09")  # Specific date
    # fetch_historical_dengue(2)  # 2 months ago for temporal lag
    
    print("=== Dengue Data Acquisition ===")
    print("Fetching latest dengue cluster data...")
    fetch_clusters()
    
    print("\nFetching historical data for temporal lag analysis...")
    fetch_historical_dengue(2)
    
    print("\nDengue data acquisition completed!")


"""
Alert Level Definitions (for reference):
- Red: High-risk area with 10 or more cases
- Yellow: High-risk area with less than 10 cases  
- Green: No new cases, under surveillance for the next 21 days
"""