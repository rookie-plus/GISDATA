# Generate lagged weather features for dengue forecasting.
# Based on research showing 2-month lag provides better model fitting

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import json
import pandas as pd
import geopandas as gpd
from typing import Dict, List, Optional
import sys
import traceback

# Path configuration
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
RAW_WEATHER = SCRIPTS_DIR.parent / "data" / "raw" / "weather"
PROCESSED_WEATHER = SCRIPTS_DIR.parent / "data" / "processed" / "weather"

def load_weather_data(data_type: str, lag_months: int = 2) -> List[Dict]:
    """
    Load weather data files with specified temporal lag.
    
    Args:
        data_type: 'temperature' or 'rainfall'
        lag_months: Number of months to lag (default: 2)
    
    Returns:
        List of weather data records
    """
    try:
        weather_dir = RAW_WEATHER / data_type
        if not weather_dir.exists():
            raise FileNotFoundError(f"Weather data directory not found: {weather_dir}")
        
        # Find files from approximately lag_months ago
        target_date = datetime.now() - timedelta(days=lag_months * 30)
        date_pattern = target_date.strftime("%Y-%m-%d")
        
        # Look for files matching the target date
        matching_files = list(weather_dir.glob(f"*{date_pattern}*.json"))
        
        if not matching_files:
            print(f"⚠️  No {data_type} files found for lag date {date_pattern}")
            print(f"   Available files: {[f.name for f in weather_dir.glob('*.json')]}")
            return []
        
        all_data = []
        for file_path in matching_files:
            print(f"Loading {data_type} data from: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # Extract actual weather readings
            if 'data' in file_data and isinstance(file_data['data'], list):
                all_data.extend(file_data['data'])
            elif isinstance(file_data, dict) and 'data' in file_data:
                all_data.append(file_data['data'])
            else:
                print(f"⚠️  Unexpected data structure in {file_path.name}")
        
        print(f"✓ Loaded {len(all_data)} {data_type} records with {lag_months}-month lag")
        return all_data
        
    except Exception as e:
        print(f"✗ Error loading {data_type} data: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise

def process_temperature_lag(lag_months: int = 2) -> pd.DataFrame:
    """Process temperature data with temporal lag for dengue modeling."""
    try:
        print(f"Processing temperature data with {lag_months}-month lag...")
        
        temp_data = load_weather_data('temperature', lag_months)
        if not temp_data:
            raise ValueError("No temperature data available for processing")
        
        # Convert to DataFrame for easier processing
        temp_df = pd.DataFrame(temp_data)
        
        # Ensure we have required columns
        required_cols = ['timestamp', 'value', 'stationId']
        missing_cols = [col for col in required_cols if col not in temp_df.columns]
        if missing_cols:
            print(f"⚠️  Missing columns in temperature data: {missing_cols}")
            print(f"   Available columns: {list(temp_df.columns)}")
        
        # Calculate minimum temperature (important for dengue modeling)
        if 'value' in temp_df.columns:
            min_temp = temp_df['value'].min()
            mean_temp = temp_df['value'].mean()
            print(f"   Temperature stats - Min: {min_temp:.2f}°C, Mean: {mean_temp:.2f}°C")
        
        return temp_df
        
    except Exception as e:
        print(f"✗ Error processing temperature lag: {str(e)}")
        raise

def process_rainfall_lag(lag_months: int = 2) -> pd.DataFrame:
    """Process rainfall data with temporal lag for dengue modeling."""
    try:
        print(f"Processing rainfall data with {lag_months}-month lag...")
        
        rainfall_data = load_weather_data('rainfall', lag_months)
        if not rainfall_data:
            raise ValueError("No rainfall data available for processing")
        
        # Convert to DataFrame for easier processing
        rainfall_df = pd.DataFrame(rainfall_data)
        
        # Ensure we have required columns
        required_cols = ['timestamp', 'value', 'stationId']
        missing_cols = [col for col in required_cols if col not in rainfall_df.columns]
        if missing_cols:
            print(f"⚠️  Missing columns in rainfall data: {missing_cols}")
            print(f"   Available columns: {list(rainfall_df.columns)}")
        
        # Calculate rainfall statistics
        if 'value' in rainfall_df.columns:
            total_rainfall = rainfall_df['value'].sum()
            mean_rainfall = rainfall_df['value'].mean()
            print(f"   Rainfall stats - Total: {total_rainfall:.2f}mm, Mean: {mean_rainfall:.2f}mm")
        
        return rainfall_df
        
    except Exception as e:
        print(f"✗ Error processing rainfall lag: {str(e)}")
        raise

def save_lagged_data(data: pd.DataFrame, data_type: str, lag_months: int = 2) -> Path:
    """Save processed lagged weather data."""
    try:
        output_dir = PROCESSED_WEATHER / data_type / "lagged"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        output_file = output_dir / f"{data_type}_lag_{lag_months}months_{timestamp}.json"
        
        # Convert DataFrame to records for JSON serialization
        records = data.to_dict('records')
        
        result = {
            "lag_months": lag_months,
            "processed_timestamp": timestamp,
            "record_count": len(records),
            "data": records
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"✓ Saved lagged {data_type} data to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"✗ Error saving lagged {data_type} data: {str(e)}")
        raise

def main():
    """Apply temporal lag processing to weather data for dengue forecasting."""
    try:
        print("=== Starting Temporal Lag Processing ===")
        print("Note: 2-month lag provides better fitting model for dengue prediction")
        
        results = {
            "temperature": None,
            "rainfall": None,
            "errors": []
        }
        
        # Process temperature with lag
        try:
            temp_df = process_temperature_lag(lag_months=2)
            temp_file = save_lagged_data(temp_df, "temperature", lag_months=2)
            results["temperature"] = str(temp_file)
        except Exception as e:
            error_msg = f"Temperature lag processing failed: {str(e)}"
            results["errors"].append(error_msg)
            print(f"✗ {error_msg}")
        
        # Process rainfall with lag
        try:
            rainfall_df = process_rainfall_lag(lag_months=2)
            rainfall_file = save_lagged_data(rainfall_df, "rainfall", lag_months=2)
            results["rainfall"] = str(rainfall_file)
        except Exception as e:
            error_msg = f"Rainfall lag processing failed: {str(e)}"
            results["errors"].append(error_msg)
            print(f"✗ {error_msg}")
        
        # Summary
        print("\n" + "="*50)
        print("TEMPORAL LAG PROCESSING SUMMARY:")
        if results["errors"]:
            print(f"⚠️  Completed with {len(results['errors'])} errors:")
            for error in results["errors"]:
                print(f"   - {error}")
            return False
        else:
            print("✓ Temporal lag processing completed successfully!")
            print(f"   Temperature file: {results['temperature']}")
            print(f"   Rainfall file: {results['rainfall']}")
            return True
            
    except Exception as e:
        print(f"✗ Fatal error in temporal lag processing: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    main()
