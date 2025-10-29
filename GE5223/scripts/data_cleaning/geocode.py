# Geocoding functions for address conversion

import geopandas as gpd
from geopy.geocoders import Nominatim
import time

def geocode_addresses(df, address_col='Location'):
    """Geocode addresses to get latitude and longitude coordinates."""
    geolocator = Nominatim(user_agent="nyc_farmers_market_analysis")
    
    latitudes = []
    longitudes = []
    
    for address in df[address_col]:
        try:
            location = geolocator.geocode(address + ", New York, NY")
            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)
            else:
                latitudes.append(None)
                longitudes.append(None)
        except:
            latitudes.append(None)
            longitudes.append(None)
        
        # Rate limiting
        time.sleep(0.1)
    
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    
    return df

def create_geodataframe(df, lat_col='latitude', lon_col='longitude'):
    """Convert DataFrame to GeoDataFrame with point geometry."""
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs='EPSG:4326'
    )
    return gdf