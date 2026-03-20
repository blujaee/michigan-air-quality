# Michigan Air Quality Dashboard

An interactive dashboard exploring air quality across Michigan, built at the intersection of computer science and public health.

## Overview

This project visualizes EPA monitoring data for three key pollutants — PM2.5, Ozone, and Nitrogen Dioxide (NO2) — across monitoring stations statewide. Each site is mapped with color intensity reflecting relative pollution levels, with hover tooltips showing site-level detail.

Built with Python, Plotly Dash, and the EPA Air Quality System (AQS) API.

## Pollutants

| Pollutant | Parameter Code | Unit |
|-----------|---------------|------|
| PM2.5 (Fine Particulate Matter) | 88101 | µg/m³ |
| Ozone | 44201 | ppm |
| Nitrogen Dioxide (NO2) | 42602 | ppb |

## Tech Stack

- **Python** — data fetching and processing
- **Pandas** — data cleaning and transformation
- **Plotly / Dash** — interactive map and dashboard
- **EPA AQS API** — air quality data source

## Running Locally

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your EPA AQS credentials:
   ```
   EPA_EMAIL=your@email.com
   EPA_KEY=your_api_key
   ```
4. Fetch and process data:
   ```bash
   python fetch_data.py
   python clean_data.py
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open `http://localhost:8050`

## Data Notes

All 2024 annual mean values for Michigan fall within the EPA "Good" classification. Dot colors reflect relative variation across the state rather than absolute AQI thresholds. Monitoring coverage varies by pollutant — PM2.5 and Ozone have the best statewide coverage.

## Data Source

[EPA Air Quality System (AQS)](https://aqs.epa.gov/aqsweb/documents/data_api.html) · State code 26 · 2024 annual summary
