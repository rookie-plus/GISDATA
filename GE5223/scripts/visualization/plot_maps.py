# Spatial distribution visualization

import matplotlib.pyplot as plt
import geopandas as gpd

def plot_spatial_distribution(data, output_dir):
    """Plot spatial distribution of farmers markets and gentrification indicators."""
    fig, ax = plt.subplots(figsize=(10, 10))
    data.plot(ax=ax, column="Median Household Income", legend=True)
    plt.savefig(os.path.join(output_dir, "spatial_distribution.png"))