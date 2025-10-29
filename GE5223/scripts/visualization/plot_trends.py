# Plot temporal trends and patterns

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_market_trends_over_time(time_series_data):
    """Plot farmers market trends over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot market count over time
    ax.plot(time_series_data['Year'], time_series_data['Market Count'], 
            marker='o', linewidth=2, label='Farmers Market Count')
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Farmers Markets')
    ax.set_title('Farmers Market Trends in NYC (2009-2023)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def plot_gentrification_indicators(gdf, indicators):
    """Plot gentrification indicators over time."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, indicator in enumerate(indicators[:4]):
        if indicator in gdf.columns:
            axes[i].plot(gdf['Year'], gdf[indicator], marker='s', linewidth=2)
            axes[i].set_title(f'{indicator} Over Time')
            axes[i].set_xlabel('Year')
            axes[i].set_ylabel(indicator)
            axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig