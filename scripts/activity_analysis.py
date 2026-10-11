from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

root = Path(__file__).resolve().parent.parent
df = pd.read_csv(root / 'Data' / 'integrated' / 'unified_dataset.csv')

d = df[df['ac_mean_co2'].notna() & df['tired'].notna() & df['productive'].notna()].copy()
d['activity'] = d['tired'] - d['productive'] + 7

pearson_r, pearson_p = stats.pearsonr(d['activity'], d['ac_mean_co2'])
spearman_rho, spearman_p = stats.spearmanr(d['activity'], d['ac_mean_co2'])
fit = stats.linregress(d['activity'], d['ac_mean_co2'])

d['group'] = pd.cut(d['activity'], [0, 5, 8, 12], labels=['low (5 or less)', 'middle (6 to 8)', 'high (9 or more)'])
groups = d.groupby('group', observed=True)['ac_mean_co2'].agg(['mean', 'count']).round(1)

# For comparison: how much does work vs home explain, and the two together?
def r2(columns, y):
    """R squared of an ordinary least squares fit with an intercept."""
    X = np.column_stack([np.ones(len(y))] + [columns[c].to_numpy(float) for c in columns])
    coef = np.linalg.lstsq(X, y.to_numpy(float), rcond=None)[0]
    fitted = (X * coef).sum(axis=1)
    return 1 - ((y - fitted) ** 2).sum() / ((y - y.mean()) ** 2).sum()


loc = d[d['ac_location_type'].notna()].copy()
loc['work'] = (loc['ac_location_type'] == 'work').astype(int)
r2_location = r2(loc[['work']], loc['ac_mean_co2'])
r2_both = r2(loc[['work', 'activity']], loc['ac_mean_co2'])

summary = pd.DataFrame([{
    'n': len(d), 'pearson_r': pearson_r, 'pearson_p': pearson_p,
    'spearman_rho': spearman_rho, 'spearman_p': spearman_p,
    'slope_ppm_per_point': fit.slope, 'slope_ci95_halfwidth': 1.96 * fit.stderr, 'r2_activity': fit.rvalue ** 2,
    'n_location': len(loc), 'r2_work_vs_home': r2_location, 'r2_work_and_activity': r2_both,
}])
results = root / 'scripts' / 'results'
results.mkdir(exist_ok=True)
summary.to_csv(results / 'activity_intensity_co2.csv', index=False)
groups.to_csv(results / 'activity_intensity_co2_groups.csv')

print(f'observations: {len(d)} (with a sensor location: {len(loc)})')
print(f'Pearson r = {pearson_r:.3f} (p = {pearson_p:.1e}), Spearman rho = {spearman_rho:.3f} (p = {spearman_p:.1e})')
print(f'slope = {fit.slope:.2f} ppm per point (95% interval +/- {1.96 * fit.stderr:.1f}), R2 = {fit.rvalue ** 2:.3f}')
print(groups)
print(f'R2 work vs home = {r2_location:.4f}, work and activity together = {r2_both:.4f}')
