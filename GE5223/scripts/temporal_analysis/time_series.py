# Time series analysis of farmers markets and gentrification indicators

import pandas as pd

def analyze_trends(data):
    """Analyze temporal trends in farmers market data."""
    trends = data.groupby("Year").agg({"Market Name": "count", "Median Household Income": "mean"})
    return trends