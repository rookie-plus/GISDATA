# Kernel Density Analysis for farmers market distribution

import numpy as np
from scipy.stats import gaussian_kde
import geopandas as gpd

def calculate_kernel_density(points_gdf, bandwidth=0.01):
    """Calculate kernel density estimation for point data."""
    # Extract coordinates
    coords = np.array([[point.x, point.y] for point in points_gdf.geometry])
    
    # Calculate KDE
    kde = gaussian_kde(coords.T, bw_method=bandwidth)
    
    return kde

def create_density_grid(kde, bounds, grid_size=100):
    """Create density grid for visualization."""
    xmin, ymin, xmax, ymax = bounds
    
    # Create grid
    x = np.linspace(xmin, xmax, grid_size)
    y = np.linspace(ymin, ymax, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Calculate density
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = kde(positions).reshape(X.shape)
    
    return X, Y, Z