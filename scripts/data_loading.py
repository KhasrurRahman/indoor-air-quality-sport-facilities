import pandas as pd
import glob
import os
from pathlib import Path

script_dir = Path(__file__).parent
data_dir = script_dir.parent / 'Data'

print("Data loading")
print("="*60)

print("\nAirControl sensors...")

aircontrol_pattern = str(data_dir / 'id*/AirControl/*/*.csv')
aircontrol_files = glob.glob(aircontrol_pattern)

print(f"Found {len(aircontrol_files)} files")

if len(aircontrol_files) > 0:
    sample_file = aircontrol_files[0]
    try:
        sample_df = pd.read_csv(sample_file, nrows=5)
        print(f"Columns: {list(sample_df.columns)}")
        full_sample = pd.read_csv(sample_file)
        print(f"Sample file rows: {len(full_sample)}")
    except Exception as e:
        print(f"Error: {e}")

print("\nAtmoTube sensors...")

atmotube_pattern = str(data_dir / 'id*/AtmoTube/*.csv')
atmotube_files = glob.glob(atmotube_pattern)

print(f"Found {len(atmotube_files)} files")

if len(atmotube_files) > 0:
    sample_file = atmotube_files[0]
    try:
        sample_df = pd.read_csv(sample_file, nrows=5)
        print(f"Columns: {list(sample_df.columns)}")
        full_sample = pd.read_csv(sample_file)
        print(f"Sample file rows: {len(full_sample)}")
    except Exception as e:
        print(f"Error: {e}")

print("\nSurvey data...")

survey_path = data_dir / 'Survey Data' / 'survey_responses.csv'

try:
    survey_df = pd.read_csv(survey_path)
    survey_df['timestamp'] = pd.to_datetime(survey_df['timestamp'])
    
    print(f"Responses: {len(survey_df)}")
    print(f"Participants: {survey_df['user_id'].nunique()}")
    print(f"Date range: {survey_df['timestamp'].min()} to {survey_df['timestamp'].max()}")
    
except Exception as e:
    print(f"Error: {e}")

print("\nStroop test data...")

stroop_path = data_dir / 'Survey Data' / 'stroop_results.csv'

try:
    stroop_df = pd.read_csv(stroop_path)
    stroop_df['timestamp'] = pd.to_datetime(stroop_df['timestamp'])
    
    print(f"Tests: {len(stroop_df)}")
    print(f"Participants: {stroop_df['user_id'].nunique()}")
    print(f"Date range: {stroop_df['timestamp'].min()} to {stroop_df['timestamp'].max()}")
    
except Exception as e:
    print(f"Error: {e}")

print("\nCreative test data...")

creative_path = data_dir / 'Survey Data' / 'creative_responses.csv'

try:
    creative_df = pd.read_csv(creative_path)
    creative_df['timestamp'] = pd.to_datetime(creative_df['timestamp'])
    
    print(f"Tests: {len(creative_df)}")
    print(f"Participants: {creative_df['user_id'].nunique()}")
    print(f"Unique objects: {creative_df['word'].nunique()}")
    print(f"Date range: {creative_df['timestamp'].min()} to {creative_df['timestamp'].max()}")
    
except Exception as e:
    print(f"Error: {e}")

print("\nSummary:")
print(f"AirControl files: {len(aircontrol_files)}")
print(f"AtmoTube files: {len(atmotube_files)}")
print(f"Survey responses: {len(survey_df) if 'survey_df' in locals() else 0}")
print(f"Stroop tests: {len(stroop_df) if 'stroop_df' in locals() else 0}")
print(f"Creative tests: {len(creative_df) if 'creative_df' in locals() else 0}")

participant_folders = glob.glob(str(data_dir / 'id*/'))
participant_count = len(participant_folders)
print(f"Participants: {participant_count}")

if participant_count > 0:
    participant_ids = [os.path.basename(f.rstrip('/')) for f in participant_folders]
    print(f"Participant IDs: {sorted(participant_ids)}")

print("\nData loading complete")
print("="*60)