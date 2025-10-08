# Fetch dengue cluster data from NEA endpoints and save to RAW storage.
# CWQ - Supports date parameters for historical data analysis

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import httpx
import json
from typing import Optional

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "dengue"

def fetch_clusters(date: Optional[str] = None) -> None:
    """Fetch dengue cluster data from Singapore Open Data API.
    
    Args:
        date: Optional date parameter for historical data (format varies by API)
              If None, fetches latest data
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_suffix = f"_{date.replace('-', '')}" if date else "_latest"
    output_file = RAW_DIR / f"dengue_clusters{date_suffix}_{timestamp}.json"
    
    # Singapore Open Data API endpoint for dengue clusters
    dataset_id = "d_dbfabf16158d1b0e1c420627c0819168"
    url = f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"
    
    print(f"Fetching dengue cluster data for: {date if date else 'latest'}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            # First, get the download URL
            response = client.get(url)
            response.raise_for_status()
            
            api_response = response.json()
            print(f"API response code: {api_response.get('code', 'unknown')}")
            
            if api_response.get('code') != 0:
                error_msg = api_response.get('errMsg', 'Unknown API error')
                print(f"API Error: {error_msg}")
                raise RuntimeError(f"API Error: {error_msg}")
            
            # Get the actual data URL
            data_url = api_response['data']['url']
            print(f"Data URL retrieved: {data_url}")
            
            # Fetch the actual dengue data
            data_response = client.get(data_url)
            data_response.raise_for_status()
            
            # Parse and save the data
            dengue_data = data_response.json()
        
        output_file.write_text(json.dumps(dengue_data, indent=2), encoding="utf-8")
        print(f"Dengue cluster data saved to: {output_file}")
        
        # Validate data structure and provide summary
        if isinstance(dengue_data, dict):
            if "features" in dengue_data:
                cluster_count = len(dengue_data["features"])
                print(f"Retrieved {cluster_count} dengue cluster features")
                
                # Count alert levels if available
                alert_levels = {}
                for feature in dengue_data["features"]:
                    if "properties" in feature and "ALERT_LEVEL" in feature["properties"]:
                        level = feature["properties"]["ALERT_LEVEL"]
                        alert_levels[level] = alert_levels.get(level, 0) + 1
                
                if alert_levels:
                    print(f"Alert level distribution: {alert_levels}")
            else:
                print("Warning: No 'features' found in dengue data")
        else:
            print(f"Warning: Unexpected data type: {type(dengue_data)}")
            
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching dengue data: {e.response.status_code}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text[:200]}...")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error fetching dengue data: {e}")
        raise

if __name__ == "__main__":
    fetch_clusters()


'''
Definition	Alert Level
High-risk area with 10 or more cases	Red
High-risk area with less than 10 cases	Yellow
No new cases, under surveillance for the next 21 days	Green
'''