# Indoor Air Quality in Sport Facilities

**Course:** 194.147 – Interdisciplinary Project in Data Science  
**Student:** Md. Khasrur Rahman (12306556)

---

## Overview

Analysis of indoor air quality (CO₂, temperature, humidity, particulate matter) in sport facilities compared to home environments. The data come from a 17-day study with fixed AirControl sensors and portable AtmoTube sensors, combined with daily well-being surveys.

---

## Project Structure

```
├── Data/
│   ├── processed/        # Cleaned sensor and survey data
│   └── integrated/       # Merged datasets ready for analysis
├── scripts/
│   ├── data_loading.py           # Load raw CSV files
│   ├── data_cleaning.py          # Remove outliers, standardise IDs
│   ├── data_integration.py       # Match sensor readings to survey timestamps
│   ├── correlation_analysis.py   # Spearman and Pearson correlations
│   ├── activity_analysis.py      # Activity proxy vs CO₂
│   └── eda/
│       └── exploratory_analysis.ipynb
├── requirements.txt
└── readme.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python scripts/data_loading.py
python scripts/data_cleaning.py
python scripts/data_integration.py
python scripts/correlation_analysis.py
python scripts/activity_analysis.py
# Then open scripts/eda/exploratory_analysis.ipynb
```

The raw data is not included in this repository. The scripts expect it in a local `Data/` folder.

---

## Data Sources

| Sensor | Type | Measures |
|---|---|---|
| AirControl | Fixed | CO₂, Temperature, Humidity |
| AtmoTube | Portable | CO₂, Temp, Humidity, VOC, PM1/PM2.5/PM10 |
| Survey | Daily | Stress, Tiredness, Productivity, Warmth, Mental demand (1–7) |
