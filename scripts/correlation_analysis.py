from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

root = Path(__file__).resolve().parent.parent
data = pd.read_csv(root / 'Data' / 'integrated' / 'survey_with_sensors.csv')

cols = ['stress', 'tired', 'productive', 'warm', 'mental_demand',
        'ac_mean_co2', 'ac_mean_temp', 'ac_mean_humidity']
d = data[cols].dropna()

spearman = d.corr(method='spearman')
pearson = d.corr(method='pearson')

results = root / 'scripts' / 'results'
results.mkdir(exist_ok=True)
spearman.to_csv(results / 'correlation_matrix_spearman.csv')
pearson.to_csv(results / 'correlation_matrix_pearson.csv')

# Figure used in the report
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(spearman, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            linewidths=1, square=True, cbar_kws={'shrink': 0.8}, ax=ax)
ax.set_title('Spearman Correlation Matrix: Air Quality vs Survey Responses',
             fontsize=14, fontweight='bold', pad=14)
plt.tight_layout()
(root / 'figures').mkdir(exist_ok=True)
plt.savefig(root / 'figures' / 'output3_spearman.png', dpi=120)
plt.close()

# Short comparison of the two methods
survey = ['stress', 'tired', 'productive', 'warm', 'mental_demand']
air = ['ac_mean_co2', 'ac_mean_temp', 'ac_mean_humidity']
diff = (spearman - pearson).abs()
print(f'observations without missing values: {len(d)}')
print(f'largest difference between the two matrices: {diff.values.max():.2f}')
strong = [(a, b) for i, a in enumerate(cols) for b in cols[i + 1:]
          if max(abs(spearman.loc[a, b]), abs(pearson.loc[a, b])) >= 0.3]
for a, b in strong:
    print(f'{a} / {b}: spearman {spearman.loc[a, b]:.2f}, pearson {pearson.loc[a, b]:.2f}')
no_warm = [s for s in survey if s != 'warm']
print('largest |rho| air quality vs survey (without perceived warmth): '
      f'spearman {spearman.loc[air, no_warm].abs().values.max():.2f}, '
      f'pearson {pearson.loc[air, no_warm].abs().values.max():.2f}')
