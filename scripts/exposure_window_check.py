from pathlib import Path

import numpy as np
import pandas as pd

root = Path(__file__).resolve().parent.parent
data = pd.read_csv(root / 'Data' / 'integrated' / 'survey_with_sensors.csv',
                   parse_dates=['timestamp'])
sensors = pd.read_csv(root / 'Data' / 'processed' / 'aircontrol_sensors_cleaned.csv',
                      usecols=['participant_id', 'datetime', 'co2', 'temperature', 'humidity'],
                      parse_dates=['datetime'])
sensors['participant_id'] = sensors['participant_id'].astype(str).str.lower()

survey = ['stress', 'tired', 'productive', 'warm', 'mental_demand']
air = {'co2': 'ac_mean_co2', 'temperature': 'ac_mean_temp', 'humidity': 'ac_mean_humidity'}
windows = [15, 30, 60]

by_person = {p: g.sort_values('datetime') for p, g in sensors.groupby('participant_id')}
for w in windows:
    for col in air:
        data[f'{col}_{w}'] = np.nan
    for i, row in data.iterrows():
        g = by_person.get(str(row['user_id_clean']))
        if g is None:
            continue
        t = g['datetime'].values
        lo = np.searchsorted(t, np.datetime64(row['timestamp'] - pd.Timedelta(minutes=w)))
        hi = np.searchsorted(t, np.datetime64(row['timestamp']), side='right')
        if hi > lo:
            for col in air:
                data.at[i, f'{col}_{w}'] = g[col].values[lo:hi].mean()

cols = survey + list(air.values()) + [f'{c}_{w}' for w in windows for c in air]
d = data[cols].dropna()

rows = []
for s in survey:
    for col, moment in air.items():
        r = {'survey': s, 'air': col, 'moment': d[s].corr(d[moment], method='spearman')}
        for w in windows:
            r[f'before_{w}min'] = d[s].corr(d[f'{col}_{w}'], method='spearman')
        rows.append(r)
out = pd.DataFrame(rows).round(3)

results = root / 'scripts' / 'results'
results.mkdir(exist_ok=True)
out.to_csv(results / 'exposure_window_correlations.csv', index=False)

before = out[[f'before_{w}min' for w in windows]]
change = before.sub(out['moment'], axis=0).abs()
flips = (np.sign(before).ne(np.sign(out['moment']), axis=0) & before.abs().gt(0.05)).sum().sum()
print(f'surveys used: {len(d)}')
print(out.to_string(index=False))
print(f'largest change in any correlation: {change.values.max():.2f}')
print(f'sign changes (ignoring |rho| <= 0.05): {flips}')
