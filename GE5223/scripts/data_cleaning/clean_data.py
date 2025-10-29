# Data cleaning and preprocessing

import pandas as pd
import numpy as np

def clean_farmers_market_data(df):
    """Clean farmers market data."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna(subset=['Market Name', 'Location'])
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    return df

def clean_census_data(df):
    """Clean census data."""
    # Remove rows with missing geographic identifiers
    df = df.dropna(subset=['GISJOIN'])
    
    # Convert numeric columns
    numeric_cols = ['Total Population', 'Median Household Income', 'Average Rent']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def apply_cpi_adjustment(data, cpi_data, base_year=2024):
    """Apply CPI adjustment to economic indicators."""
    # Calculate inflation factors
    cpi_data['inflation_factor'] = cpi_data['CPI-U'] / cpi_data.loc[cpi_data['Year'] == base_year, 'CPI-U'].values[0]
    
    # Merge with data
    data = data.merge(cpi_data[['Year', 'inflation_factor']], on='Year', how='left')
    
    # Adjust economic indicators
    if 'Median Household Income' in data.columns:
        data['Median Household Income Adjusted'] = data['Median Household Income'] * data['inflation_factor']
    
    if 'Average Rent' in data.columns:
        data['Average Rent Adjusted'] = data['Average Rent'] * data['inflation_factor']
    
    return data