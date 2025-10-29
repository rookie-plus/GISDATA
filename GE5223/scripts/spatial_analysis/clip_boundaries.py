# Clip data to NYC boundaries

import geopandas as gpd

def clip_to_nyc(data, boundary_path):
    """Clip input data to NYC borough boundaries."""
    nyc_boundary = gpd.read_file(boundary_path)
    clipped_data = gpd.clip(data, nyc_boundary)
    return clipped_data