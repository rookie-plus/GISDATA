# Correlation analysis between farmers markets and gentrification

import pandas as pd
from scipy.stats import pearsonr, spearmanr
import numpy as np

def calculate_correlation(market_data, gentrification_data, method='pearson'):
    """Calculate correlation between market density and gentrification indicators."""
    correlations = {}
    
    # Merge data on common identifier (e.g., neighborhood ID)
    merged_data = pd.merge(market_data, gentrification_data, on='GISJOIN', how='inner')
    
    # Calculate correlations for each indicator
    indicators = ['Median Household Income', 'Average Rent', 'Total Population', 'gentrification_score']
    
    for indicator in indicators:
        if indicator in merged_data.columns:
            if method == 'pearson':
                corr, p_value = pearsonr(merged_data['Market Count'], merged_data[indicator])
            else:
                corr, p_value = spearmanr(merged_data['Market Count'], merged_data[indicator])
            
            correlations[indicator] = {
                'correlation': corr,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    return correlations

def calculate_spatial_lag_correlation(gdf, market_col, indicator_col):
    """Calculate spatial lag correlation accounting for spatial dependence."""
    # This would require more advanced spatial econometrics
    # Placeholder for spatial regression implementation
    pass