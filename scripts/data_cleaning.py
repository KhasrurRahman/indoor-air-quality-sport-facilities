import pandas as pd
import glob
import os
import re
from pathlib import Path
import numpy as np

script_dir = Path(__file__).parent
data_dir = script_dir.parent / 'Data'
output_dir = script_dir.parent / 'Data' / 'processed'
output_dir.mkdir(exist_ok=True)

print("Data cleaning")
print("="*60)

def standardize_id(user_id):
    if pd.isna(user_id):
        return None
    user_id = str(user_id).strip()
    user_id_clean = re.sub(r'^id', '', user_id, flags=re.IGNORECASE)
    numbers = re.findall(r'\d+', user_id_clean)
    if numbers:
        return f"id{numbers[0].zfill(3)}"
    return user_id.lower()

def count_fluency(text):
    if pd.isna(text) or text == '':
        return 0
    text = str(text).strip()
    lines = text.split('\n')
    responses = []
    for line in lines:
        for part in line.split(','):
            cleaned = part.strip()
            if cleaned and cleaned not in ['', '?', '.']:
                responses.append(cleaned)
    return len(responses)

print("\nSurvey data...", end=" ")

survey_df = pd.read_csv(data_dir / 'Survey Data' / 'survey_responses.csv')
survey_df['user_id_clean'] = survey_df['user_id'].apply(standardize_id)
survey_df['timestamp'] = pd.to_datetime(survey_df['timestamp'])

survey_df = survey_df.dropna(subset=['stress', 'tired', 'productive', 'warm', 'mental_demand'], how='all')

for col in ['stress', 'tired', 'productive', 'warm', 'mental_demand']:
    survey_df.loc[(survey_df[col] < 1) | (survey_df[col] > 7), col] = np.nan

survey_df.to_csv(output_dir / 'survey_responses_cleaned.csv', index=False)
print(f"{len(survey_df)} rows")

print("Stroop data...", end=" ")

stroop_df = pd.read_csv(data_dir / 'Survey Data' / 'stroop_results.csv')
stroop_df['user_id_clean'] = stroop_df['user_id'].apply(standardize_id)
stroop_df['timestamp'] = pd.to_datetime(stroop_df['timestamp'])

stroop_df = stroop_df[
    (stroop_df['avg_congruent_rt'] >= 0.1) & (stroop_df['avg_congruent_rt'] <= 10) &
    (stroop_df['avg_incongruent_rt'] >= 0.1) & (stroop_df['avg_incongruent_rt'] <= 10)
]

stroop_df.to_csv(output_dir / 'stroop_results_cleaned.csv', index=False)
print(f"{len(stroop_df)} rows")

print("Creative data...", end=" ")

creative_df = pd.read_csv(data_dir / 'Survey Data' / 'creative_responses.csv')
creative_df['user_id_clean'] = creative_df['user_id'].apply(standardize_id)
creative_df['timestamp'] = pd.to_datetime(creative_df['timestamp'])
creative_df['fluency'] = creative_df['responses'].apply(count_fluency)
creative_df = creative_df[creative_df['fluency'] > 0]

creative_df.to_csv(output_dir / 'creative_responses_cleaned.csv', index=False)
print(f"{len(creative_df)} rows")

print("AirControl sensors...", end=" ")

aircontrol_files = glob.glob(str(data_dir / 'id*/AirControl/*/*.csv'))
aircontrol_dfs = []

for file_path in aircontrol_files:
    try:
        parts = file_path.split('/')
        participant_id = None
        location_type = None
        
        for part in parts:
            if part.startswith('id') and len(part) > 2:
                participant_id = part
            if 'arbeit' in part.lower():
                location_type = 'work'
            elif 'house' in part.lower() or 'hause' in part.lower():
                location_type = 'home'
        
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(
            df['D_M_YYYY'].astype(str) + ' ' + df['TIME[HH:mm:ss]'].astype(str),
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        df['participant_id'] = participant_id
        df['location_type'] = location_type
        df['sensor_type'] = 'AirControl'
        
        df = df.rename(columns={
            'CO2[ppm]': 'co2',
            'Temp[C]': 'temperature',
            'RH[%]': 'humidity'
        })
        
        df = df[
            (df['co2'] >= 300) & (df['co2'] <= 5000) &
            (df['temperature'] >= 10) & (df['temperature'] <= 40) &
            (df['humidity'] >= 10) & (df['humidity'] <= 90)
        ]
        df = df.dropna(subset=['datetime'])
        
        if len(df) > 0:
            aircontrol_dfs.append(df)
    except:
        continue

if aircontrol_dfs:
    aircontrol_combined = pd.concat(aircontrol_dfs, ignore_index=True)
    aircontrol_combined.to_csv(output_dir / 'aircontrol_sensors_cleaned.csv', index=False)
    print(f"{len(aircontrol_combined)} rows")

print("AtmoTube sensors...", end=" ")

atmotube_files = glob.glob(str(data_dir / 'id*/AtmoTube/*.csv'))
atmotube_dfs = []

for file_path in atmotube_files:
    try:
        filename = os.path.basename(file_path)
        participant_match = re.search(r'id(\d+)', filename, re.IGNORECASE)
        participant_id = participant_match.group(0).lower() if participant_match else None
        
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(df['Date'], errors='coerce')
        df['participant_id'] = participant_id
        df['sensor_type'] = 'AtmoTube'
        
        df = df.rename(columns={
            'VOC, ppm': 'voc',
            'AQS': 'aqs',
            'Temperature, ˚C': 'temperature',
            'Humidity, %': 'humidity',
            'Pressure, hPa': 'pressure',
            'PM1, ug/m³': 'pm1',
            'PM2.5, ug/m³': 'pm25',
            'PM10, ug/m³': 'pm10'
        })
        
        df = df[
            (df['temperature'] >= 10) & (df['temperature'] <= 40) &
            (df['humidity'] >= 10) & (df['humidity'] <= 90)
        ]
        if 'pm25' in df.columns:
            df = df[(df['pm25'] >= 0) & (df['pm25'] <= 500)]
        
        df = df.dropna(subset=['datetime'])
        
        if len(df) > 0:
            atmotube_dfs.append(df)
    except:
        continue

if atmotube_dfs:
    atmotube_combined = pd.concat(atmotube_dfs, ignore_index=True)
    atmotube_combined.to_csv(output_dir / 'atmotube_sensors_cleaned.csv', index=False)
    print(f"{len(atmotube_combined)} rows")

print("\nCleaning complete. Files saved to Data/processed/")
print("="*60)