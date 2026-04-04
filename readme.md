# Indoor Air Quality in Sport Facilities

**Course:** 194.147 – Interdisciplinary Project in Data Science  
**Student:** Md. Khasrur Rahman (12306556)  
**Supervisor:** Ass.-Prof. Milica Vujovic, PhD | Dr. Florina Piroi

---

## Overview

Analysis of indoor air quality (CO₂, temperature, humidity, particulate matter) in sport facilities compared to home environments. Data collected from 22 participants over 17 days using fixed AirControl sensors and portable AtmoTube sensors, combined with daily well-being surveys.

---

## Project Structure

```
├── Data/
│   ├── processed/        # Cleaned sensor and survey data
│   └── integrated/       # Merged datasets ready for analysis
├── scripts/
│   ├── data_loading.py       # Load raw CSV files
│   ├── data_cleaning.py      # Remove outliers, standardise IDs
│   ├── data_integration.py   # Match sensor readings to survey timestamps
│   └── eda/
│       └── exploratory_analysis.ipynb
├── figures/              # Output plots
├── report/               # Final PDF report
└── readme.md
```

---

## How to Run

```bash
python scripts/data_loading.py
python scripts/data_cleaning.py
python scripts/data_integration.py
# Then open scripts/eda/exploratory_analysis.ipynb
```

---

## Data Sources

| Sensor | Type | Measures |
|---|---|---|
| AirControl | Fixed | CO₂, Temperature, Humidity |
| AtmoTube | Portable | CO₂, Temp, Humidity, VOC, PM1/PM2.5/PM10 |
| Survey | Daily | Stress, Tiredness, Productivity, Warmth, Mental demand (1–7) |

---

## Study Details

- **Participants:** 22 (id088 – id108)
- **Period:** June 29 – July 15, 2025 (17 days)
- **Locations:** Home and sport facility (gym/climbing hall) per participant
- **Surveys collected:** 713 responses
