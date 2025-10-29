# Spatial autocorrelation analysis using Moran's I and LISA

import libpysal as lps
from esda.moran import Moran, Moran_Local
import geopandas as gpd
import numpy as np

def calculate_morans_i(gdf, variable_col, weights_method='queen'):
    """Calculate global Moran's I for spatial autocorrelation."""
    # Create spatial weights matrix
    if weights_method == 'queen':
        w = lps.weights.Queen.from_dataframe(gdf)
    elif weights_method == 'rook':
        w = lps.weights.Rook.from_dataframe(gdf)
    else:
        w = lps.weights.KNN.from_dataframe(gdf, k=5)
    
    # Calculate Moran's I
    y = gdf[variable_col].values
    moran = Moran(y, w)
    
    return moran

def calculate_local_morans_i(gdf, variable_col, weights_method='queen'):
    """Calculate local Moran's I (LISA) for hotspot detection."""
    # Create spatial weights matrix
    if weights_method == 'queen':
        w = lps.weights.Queen.from_dataframe(gdf)
    else:
        w = lps.weights.Rook.from_dataframe(gdf)
    
    # Calculate Local Moran's I
    y = gdf[variable_col].values
    lisa = Moran_Local(y, w)
    
    return lisa