# Plot correlation analysis results

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_correlation_matrix(correlation_results):
    """Plot correlation matrix heatmap."""
    # Extract correlation values
    indicators = list(correlation_results.keys())
    corr_values = [correlation_results[ind]['correlation'] for ind in indicators]
    
    # Create correlation matrix (simplified)
    corr_matrix = np.array(corr_values).reshape(-1, 1)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, xticklabels=['Market Count'], 
                yticklabels=indicators, cmap='coolwarm', center=0,
                ax=ax)
    ax.set_title('Correlation: Farmers Markets vs Gentrification Indicators')
    
    return fig

def plot_scatter_with_correlation(market_data, gentrification_data, indicator):
    """Plot scatter plot with correlation line."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax.scatter(market_data['Market Count'], gentrification_data[indicator], 
               alpha=0.6, s=50)
    
    # Add correlation line
    z = np.polyfit(market_data['Market Count'], gentrification_data[indicator], 1)
    p = np.poly1d(z)
    ax.plot(market_data['Market Count'], p(market_data['Market Count']), 
            "r--", alpha=0.8)
    
    ax.set_xlabel('Farmers Market Count')
    ax.set_ylabel(indicator)
    ax.set_title(f'Farmers Markets vs {indicator}')
    ax.grid(True, alpha=0.3)
    
    return fig