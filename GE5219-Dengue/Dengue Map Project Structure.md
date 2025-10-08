# Dengue Map Project Structure

```
GE5219_Dengue/
│
├── data/
│   ├── raw/
│   │   ├── dengue/                      # Daily dengue cluster data
│   │   ├── weather/                     # 5-minute weather data updates
│   │   │   ├── rainfall/
│   │   │   └── temperature/
│   │   ├── boundaries/                  # Subzone boundaries
│   │   ├── population/                  # Population data by subzone
│   │   └── satellite/                   # Raw satellite imagery for NDVI
│   │
│   ├── processed/
│   │   ├── dengue/
│   │   ├── weather/
│   │   │   ├── current/
│   │   │   └── lagged/                  # 2-month lagged weather data
│   │   ├── ndvi/                        # Processed vegetation density
│   │   └── population_density/
│   │
│   └── aggregated/                      # Data aggregated by subzones
│
├── scripts/
│   ├── acquisition/                     # Data collection scripts
│   │   ├── fetch_dengue.py
│   │   ├── fetch_weather.py
│   │   └── fetch_satellite.py
│   │
│   ├── processing/                      # Data cleaning and processing
│   │   ├── create_ndvi.py
│   │   ├── calculate_population_density.py
│   │   ├── apply_temporal_lag.py
│   │   └── interpolate_surfaces.py
│   │
│   └── analysis/                        # Risk calculation scripts
│       ├── ahp_model.py
│       └── risk_score_calculator.py
│
├── models/                              # Saved model parameters and weights
│   └── ahp_weights/
│
├── visualization/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── app.js                           # Main visualization code
│
├── logs/                                # Application logs
│
├── config/                              # Configuration files
│   ├── api_config.json
│   └── app_config.json
│
├── tests/                               # Unit and integration tests
│
├── docs/                                # Documentation
│
├── .gitignore
├── README.md
├── requirements.md                  # Project requirements   
├── dependencies.txt                     # Python dependencies
└── main.py                              # Application entry point
```