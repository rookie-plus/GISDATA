# Merge different datasets for analysis

import pandas as pd
import geopandas as gpd

def merge_farmers_market_with_census(farmers_market_gdf, census_gdf, buffer_distance=500):
    """Merge farmers market data with census data using spatial join."""
    # Create buffer around farmers markets
    farmers_market_buffered = farmers_market_gdf.copy()
    farmers_market_buffered['geometry'] = farmers_market_buffered.geometry.buffer(buffer_distance)
    
    # Spatial join
    merged_gdf = gpd.sjoin(
        farmers_market_buffered, 
        census_gdf, 
        how='left', 
        predicate='intersects'
    )
    
    return merged_gdf

def aggregate_data_by_neighborhood(merged_gdf, group_col='GISJOIN'):
    """Aggregate data by neighborhood/census tract."""
    aggregated = merged_gdf.groupby(group_col).agg({
        'Market Name': 'count',
        'Median Household Income': 'mean',
        'Average Rent': 'mean',
        'Total Population': 'mean'
    }).reset_index()
    
    aggregated = aggregated.rename(columns={'Market Name': 'Market Count'})
    
    return aggregated