# System Requirements

- Python 3.11+
- Node.js 18+ (for front-end tooling)
- GDAL 3.x with Python bindings
- PostgreSQL + PostGIS (optional, for spatial persistence)
- Access to NEA dengue API and weather endpoints
# Research Plan
## Project Goal: To develop an automated workflow that produces a real-time, evidence-based dengue risk map for Singapore, visualized through an interactive web dashboard.

### **Data:**

**Active Dengue Cases**https://data.gov.sg/datasets?query=Dengue+Clusters+(GEOJSON)&resultId=d_dbfabf16158d1b0e1c420627c0819168&page=1&sidebar=false - updated daily

**Real-time Rainfall** https://data.gov.sg/datasets/d_6580738cdd7db79374ed3152159fbd69/view - updated every 5 minutes

**Real-time Air Temperature** https://data.gov.sg/datasets/d_66b77726bbae1b33f218db60ff5861f0/view - updated every 5 minutes

**Subzone boundaries**  https://data.gov.sg/datasets?query=Boundary&page=1&sidebar=false&resultId=d_8594ae9ff96d0c708bc2af633048edfb
**Vegetation Density (NDVI)**

**Population by subzone** https://data.gov.sg/datasets/d_e7ae90176a68945837ad67892b898466/view

### **Methodology:**

**Variables**:

Dengue Cases

rainfall lagging 2 months

(lowest) air temperature lagging 2 months

population density

Vegetation Density (NDVI)

### —WORKFLOW STARTS HERE—

**Acquire Live Data**

Python requests API → **lagging temperature and rainfall by two months provided a better fitting model**.

![image.png](attachment:aa232f6b-8c74-4095-8842-9276cdd99e2b:image.png)

~~Sentinel-2 imagery (or other available ones)~~

**Process, Clean, and Prepare Data**

pandas, Geopandas, Arcpy

Create the NDVI surface

Project all to SVY21

Calculate population density

Interpolate rainfall & temperature Surfaces (Kriging)

Aggregate All Data to Subzones

**Weighted Risk Score Calculation**

ArcPy

Determine Variable Weights with Analytical Hierarchy Process (AHP)

model AHP through space-time scan statistics using historical data

Calculate the weighted Risk Score

**Visualization & Deployment**

HTML/JavaScript Front-End

Leaflet/Mapbox…?

---

**Contribution:**

clj - HTML/JS visualization & deployment

cwq - Live data acquisition, literature review

Rachel - process, clean, and prepare data

xsx - Project design, literature review, data collection, process historical data, modify & validate the AHP model through space-time scan statistics, normalize & calculate weighted Risk Score

ybs - Aggregate Data & Create the NDVI surface, HTML/JS visualization & deployment

---

**Proposal Presentation:**

clj - p7

cwq - p8

Rachel - p2-3

xsx - p4-5

ybs - p6 & 9