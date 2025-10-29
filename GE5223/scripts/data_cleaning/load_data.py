# Load raw data from CSV/Excel files

import pandas as pd
import os

def load_raw_data(data_dir):
    """Load raw data files from the specified directory."""
    farmers_market = pd.read_excel(os.path.join(data_dir, "Historical_FarmersMarkets_2009-2020.xlsx"))
    census_data = pd.read_csv(os.path.join(data_dir, "nhgis0003_shape/nhgis0003_blockgroupcsv/nhgis0003_ds172_2010_blck_grp.csv"))
    cpi_data = pd.read_csv(os.path.join(data_dir, "CPI-U_Annual_Average_1990-2024.csv"))
    
    return {
        "farmers_market": farmers_market,
        "census_data": census_data,
        "cpi_data": cpi_data
    }