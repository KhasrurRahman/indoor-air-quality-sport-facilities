
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta

script_dir = Path(__file__).parent
data_dir = script_dir.parent / 'Data'
processed_dir = data_dir / 'processed'
output_dir = data_dir / 'integrated'
output_dir.mkdir(exist_ok=True)

print("Data integration")
print("="*60)

def standardize_id(user_id):
    if pd.isna(user_id):
        return None
    user_id = str(user_id).strip().lower()
    if user_id.startswith('id'):
        return user_id
    numbers = ''.join(filter(str.isdigit, user_id))
    if numbers:
        return f"id{numbers.zfill(3)}"
    return user_id

def match_sensor_data(survey_time, sensor_df, participant_id, window_minutes=30):
    start_time = survey_time - timedelta(minutes=window_minutes)
    end_time = survey_time + timedelta(minutes=window_minutes)
    
    mask = (
        (sensor_df['datetime'] >= start_time) & 
        (sensor_df['datetime'] <= end_time) &
        (sensor_df['participant_id'] == participant_id)
    )
    
    matched = sensor_df[mask]
    if len(matched) == 0:
        return None
    
    return {
        'mean_co2': matched['co2'].mean() if 'co2' in matched.columns else None,
        'mean_temp': matched['temperature'].mean(),
        'mean_humidity': matched['humidity'].mean(),
        'mean_voc': matched['voc'].mean() if 'voc' in matched.columns else None,
        'mean_pm25': matched['pm25'].mean() if 'pm25' in matched.columns else None,
        'mean_aqs': matched['aqs'].mean() if 'aqs' in matched.columns else None,
        'location_type': matched['location_type'].iloc[0] if 'location_type' in matched.columns else None,
        'sensor_count': len(matched)
    }

def match_test_data(survey_time, test_df, participant_id, window_minutes=10):
    start_time = survey_time - timedelta(minutes=window_minutes)
    end_time = survey_time + timedelta(minutes=window_minutes)
    
    mask = (
        (test_df['timestamp'] >= start_time) & 
        (test_df['timestamp'] <= end_time) &
        (test_df['user_id_clean'] == participant_id)
    )
    
    matched = test_df[mask]
    if len(matched) == 0:
        return None
    
    matched['time_diff'] = abs((matched['timestamp'] - survey_time).dt.total_seconds())
    closest = matched.loc[matched['time_diff'].idxmin()]
    
    return closest.to_dict()

print("\nLoading cleaned data...", end=" ")

survey_df = pd.read_csv(processed_dir / 'survey_responses_cleaned.csv')
stroop_df = pd.read_csv(processed_dir / 'stroop_results_cleaned.csv')
creative_df = pd.read_csv(processed_dir / 'creative_responses_cleaned.csv')
aircontrol_df = pd.read_csv(processed_dir / 'aircontrol_sensors_cleaned.csv')
atmotube_df = pd.read_csv(processed_dir / 'atmotube_sensors_cleaned.csv')

survey_df['timestamp'] = pd.to_datetime(survey_df['timestamp'])
stroop_df['timestamp'] = pd.to_datetime(stroop_df['timestamp'])
creative_df['timestamp'] = pd.to_datetime(creative_df['timestamp'])
aircontrol_df['datetime'] = pd.to_datetime(aircontrol_df['datetime'])
atmotube_df['datetime'] = pd.to_datetime(atmotube_df['datetime'])

aircontrol_df['participant_id'] = aircontrol_df['participant_id'].apply(standardize_id)
atmotube_df['participant_id'] = atmotube_df['participant_id'].apply(standardize_id)

print(f"{len(survey_df)} surveys, {len(stroop_df)} Stroop, {len(creative_df)} Creative")

print("Merging survey data with sensors...", end=" ")

survey_sensor_data = []

for idx, row in survey_df.iterrows():
    participant_id = row['user_id_clean']
    survey_time = row['timestamp']
    
    ac_data = match_sensor_data(survey_time, aircontrol_df, participant_id)
    at_data = match_sensor_data(survey_time, atmotube_df, participant_id)
    
    merged_row = row.to_dict()
    
    if ac_data:
        merged_row.update({f'ac_{k}': v for k, v in ac_data.items()})
    
    if at_data:
        merged_row.update({f'at_{k}': v for k, v in at_data.items()})
    
    survey_sensor_data.append(merged_row)

survey_merged = pd.DataFrame(survey_sensor_data)
survey_merged.to_csv(output_dir / 'survey_with_sensors.csv', index=False)
print(f"{len(survey_merged)} rows")

print("Merging Stroop data with sensors...", end=" ")

stroop_sensor_data = []

for idx, row in stroop_df.iterrows():
    participant_id = row['user_id_clean']
    stroop_time = row['timestamp']
    
    ac_data = match_sensor_data(stroop_time, aircontrol_df, participant_id)
    at_data = match_sensor_data(stroop_time, atmotube_df, participant_id)
    
    merged_row = row.to_dict()
    
    if ac_data:
        merged_row.update({f'ac_{k}': v for k, v in ac_data.items()})
    
    if at_data:
        merged_row.update({f'at_{k}': v for k, v in at_data.items()})
    
    stroop_sensor_data.append(merged_row)

stroop_merged = pd.DataFrame(stroop_sensor_data)
stroop_merged.to_csv(output_dir / 'stroop_with_sensors.csv', index=False)
print(f"{len(stroop_merged)} rows")

print("Merging Creative data with sensors...", end=" ")

creative_sensor_data = []

for idx, row in creative_df.iterrows():
    participant_id = row['user_id_clean']
    creative_time = row['timestamp']
    
    ac_data = match_sensor_data(creative_time, aircontrol_df, participant_id)
    at_data = match_sensor_data(creative_time, atmotube_df, participant_id)
    
    merged_row = row.to_dict()
    
    if ac_data:
        merged_row.update({f'ac_{k}': v for k, v in ac_data.items()})
    
    if at_data:
        merged_row.update({f'at_{k}': v for k, v in at_data.items()})
    
    creative_sensor_data.append(merged_row)

creative_merged = pd.DataFrame(creative_sensor_data)
creative_merged.to_csv(output_dir / 'creative_with_sensors.csv', index=False)
print(f"{len(creative_merged)} rows")

print("Creating unified dataset...", end=" ")
stroop_matched = []
for idx, row in survey_merged.iterrows():
    participant_id = row['user_id_clean']
    survey_time = row['timestamp']
    
    stroop_data = match_test_data(survey_time, stroop_df, participant_id, window_minutes=10)
    
    if stroop_data:
        stroop_matched.append({
            'accuracy': stroop_data.get('accuracy'),
            'avg_congruent_rt': stroop_data.get('avg_congruent_rt'),
            'avg_incongruent_rt': stroop_data.get('avg_incongruent_rt'),
            'stroop_effect': stroop_data.get('stroop_effect')
        })
    else:
        stroop_matched.append({
            'accuracy': None,
            'avg_congruent_rt': None,
            'avg_incongruent_rt': None,
            'stroop_effect': None
        })

stroop_df_matched = pd.DataFrame(stroop_matched)

creative_matched = []
for idx, row in survey_merged.iterrows():
    participant_id = row['user_id_clean']
    survey_time = row['timestamp']
    
    start_time = survey_time - timedelta(minutes=10)
    end_time = survey_time + timedelta(minutes=10)
    
    mask = (
        (creative_df['timestamp'] >= start_time) & 
        (creative_df['timestamp'] <= end_time) &
        (creative_df['user_id_clean'] == participant_id)
    )
    
    matched = creative_df[mask]
    
    if len(matched) > 0:
        total_fluency = matched['fluency'].sum()
    else:
        total_fluency = None
    
    creative_matched.append({'total_fluency': total_fluency})

creative_df_matched = pd.DataFrame(creative_matched)

unified = survey_merged.copy()
unified['accuracy'] = stroop_df_matched['accuracy'].values
unified['avg_congruent_rt'] = stroop_df_matched['avg_congruent_rt'].values
unified['avg_incongruent_rt'] = stroop_df_matched['avg_incongruent_rt'].values
unified['stroop_effect'] = stroop_df_matched['stroop_effect'].values
unified['total_fluency'] = creative_df_matched['total_fluency'].values

unified.to_csv(output_dir / 'unified_dataset.csv', index=False)
print(f"{len(unified)} rows")

print("\nSummary:")
print(f"Total surveys: {len(unified)}")
print(f"With Stroop data: {unified['accuracy'].notna().sum()}")
print(f"With Creative data: {unified['total_fluency'].notna().sum()}")
print(f"With AirControl data: {unified['ac_mean_co2'].notna().sum()}")
print(f"With AtmoTube data: {unified['at_mean_temp'].notna().sum()}")
print("\nIntegration complete. Files saved to Data/integrated/")
print("="*60)