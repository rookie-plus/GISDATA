# GE5223 Scripts Package
# Spatial analysis of NYC farmers markets and gentrification

__version__ = "1.0.0"
__author__ = "GE5223 Team"

# Import main modules for easier access
from .data_cleaning import load_data, clean_data, geocode, merge_data
from .spatial_analysis import clip_boundaries, density_analysis, spatial_autocorrelation, hotspot_analysis
from .temporal_analysis import time_series, gentrification_trends, correlation_analysis
from .visualization import plot_maps, plot_trends, plot_correlation