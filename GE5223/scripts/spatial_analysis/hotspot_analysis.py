# Hotspot analysis for gentrification patterns

import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN

def identify_gentrification_hotspots(gdf, income_col, rent_col, population_col):
    """Identify gentrification hotspots based on economic indicators."""
    # Calculate change rates (if time series data available)
    # For now, use current values as indicators
    
    # Normalize indicators
    indicators = gdf[[income_col, rent_col, population_col]].copy()
    indicators = (indicators - indicators.mean()) / indicators.std()
    
    # Apply clustering
    clustering = DBSCAN(eps=0.5, min_samples=5).fit(indicators)
    gdf['hotspot_cluster'] = clustering.labels_
    
    return gdf

def calculate_gentrification_score(gdf, income_weight=0.4, rent_weight=0.4, pop_weight=0.2):
    """Calculate gentrification score for each neighborhood."""
    # Normalize indicators
    income_norm = (gdf['Median Household Income'] - gdf['Median Household Income'].mean()) / gdf['Median Household Income'].std()
    rent_norm = (gdf['Average Rent'] - gdf['Average Rent'].mean()) / gdf['Average Rent'].std()
    pop_norm = (gdf['Total Population'] - gdf['Total Population'].mean()) / gdf['Total Population'].std()
    
    # Calculate score
    gdf['gentrification_score'] = (
        income_norm * income_weight + 
        rent_norm * rent_weight + 
        pop_norm * pop_weight
    )
    
    return gdf