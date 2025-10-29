# Analyze gentrification trends over time

import pandas as pd
import numpy as np

def calculate_growth_rates(time_series_data, variable_cols):
    """Calculate growth rates for gentrification indicators."""
    growth_rates = {}
    
    for col in variable_cols:
        if col in time_series_data.columns:
            # Sort by year
            sorted_data = time_series_data.sort_values('Year')
            
            # Calculate annual growth rate
            sorted_data[f'{col}_growth_rate'] = sorted_data[col].pct_change() * 100
            growth_rates[col] = sorted_data
    
    return growth_rates

def identify_gentrification_periods(growth_data, threshold=5.0):
    """Identify periods of significant gentrification."""
    gentrification_periods = []
    
    for col, data in growth_data.items():
        # Find years with growth above threshold
        high_growth_years = data[data[f'{col}_growth_rate'] > threshold]['Year'].tolist()
        gentrification_periods.extend(high_growth_years)
    
    return list(set(gentrification_periods))