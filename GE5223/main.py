# GE5223 - NYC Farmers Markets and Gentrification Analysis
# Main entry point for the project

import os
from scripts.data_cleaning.load_data import load_raw_data
from scripts.data_cleaning.clean_data import clean_data
from scripts.spatial_analysis.clip_boundaries import clip_to_nyc
from scripts.spatial_analysis.density_analysis import calculate_kde
from scripts.temporal_analysis.time_series import analyze_trends
from scripts.visualization.plot_maps import plot_spatial_distribution

# Initialize project paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Main workflow
def main():
    # Step 1: Data loading and cleaning
    raw_data = load_raw_data(DATA_DIR)
    cleaned_data = clean_data(raw_data)
    
    # Step 2: Spatial analysis
    nyc_data = clip_to_nyc(cleaned_data)
    density_results = calculate_kde(nyc_data)
    
    # Step 3: Temporal analysis
    trends = analyze_trends(nyc_data)
    
    # Step 4: Visualization
    plot_spatial_distribution(density_results, OUTPUT_DIR)

if __name__ == "__main__":
    main()