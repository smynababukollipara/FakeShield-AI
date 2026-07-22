# ─────────────────────────────────────────────────────────────
# data/explore_data.py
# A plain Python version of the notebook exploration.
# Run it with:  python data/explore_data.py
# (No Jupyter needed — works anywhere)
# ─────────────────────────────────────────────────────────────

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid')

# ── Make sure the output folder exists ────────────────────────
os.makedirs('data/processed', exist_ok=True)

# ══════════════════════════════════════════════════════════════
# STEP 1 — Load the dataset
# ══════════════════════════════════════════════════════════════
print('\n📂 Loading dataset...')

df = pd.read_csv('data/raw/news.csv')

# Map text labels to numbers: REAL→0, FAKE→1
df['label_num'] = df['label'].map({'REAL': 0, 'FAKE': 1})

real_count = (df['label'] == 'REAL').sum()
fake_count = (df['label'] == 'FAKE').sum()

print(f'✅ Loaded {len(df):,} articles')
print(f'   REAL : {real_count:,}')
print(f'   FAKE : {fake_count:,}')

# ══════════════════════════════════════════════════════════════
# STEP 2 — Basic info
# ══════════════════════════════════════════════════════════════
print('\n📋 Column names:', df.columns.tolist())
print('   Shape (rows × columns):', df.shape)

print('\n🔍 Missing values per column:')
print(df.isnull().sum().to_string())

# ══════════════════════════════════════════════════════════════
# STEP 3 — Print sample articles
# ══════════════════════════════════════════════════════════════
print('\n' + '=' * 60)
print('🔴  FAKE ARTICLE SAMPLE')
print('=' * 60)
fake_row = df[df['label'] == 'FAKE'].iloc[0]
print('Title:', fake_row['title'])
print('Text (first 400 chars):')
print(str(fake_row['text'])[:400])

print('\n' + '=' * 60)
print('🟢  REAL ARTICLE SAMPLE')
print('=' * 60)
real_row = df[df['label'] == 'REAL'].iloc[0]
print('Title:', real_row['title'])
print('Text (first 400 chars):')
print(str(real_row['text'])[:400])

# ══════════════════════════════════════════════════════════════
# STEP 4 — Chart 1: REAL vs FAKE count
# ══════════════════════════════════════════════════════════════
print('\n📊 Saving chart 1: class balance...')

counts = df['label'].value_counts()
plt.figure(figsize=(6, 4))
bars = plt.bar(counts.index, counts.values,
               color=['#2ecc71', '#e74c3c'], edgecolor='black', width=0.5)
for bar, val in zip(bars, counts.values):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 30,
             f'{val:,}', ha='center', fontsize=12, fontweight='bold')
plt.title('Article Count: REAL vs FAKE', fontsize=14)
plt.ylabel('Number of Articles')
plt.tight_layout()
plt.savefig('data/processed/chart_class_balance.png', dpi=100)
plt.close()
print('   ✅ Saved → data/processed/chart_class_balance.png')

# ══════════════════════════════════════════════════════════════
# STEP 5 — Chart 2: Text length comparison
# ══════════════════════════════════════════════════════════════
print('\n📊 Saving chart 2: text length...')

df['text_length'] = df['text'].fillna('').apply(len)

avg_real = int(df[df['label'] == 'REAL']['text_length'].mean())
avg_fake = int(df[df['label'] == 'FAKE']['text_length'].mean())
print(f'   Average length — REAL: {avg_real:,} characters')
print(f'   Average length — FAKE: {avg_fake:,} characters')

plt.figure(figsize=(9, 4))
df[df['label'] == 'REAL']['text_length'].plot(
    kind='hist', bins=50, alpha=0.6, color='#2ecc71', label='REAL')
df[df['label'] == 'FAKE']['text_length'].plot(
    kind='hist', bins=50, alpha=0.6, color='#e74c3c', label='FAKE')
plt.title('Article Length: REAL vs FAKE', fontsize=14)
plt.xlabel('Number of Characters')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('data/processed/chart_text_length.png', dpi=100)
plt.close()
print('   ✅ Saved → data/processed/chart_text_length.png')

# ══════════════════════════════════════════════════════════════
# STEP 6 — Word clouds
# ══════════════════════════════════════════════════════════════
print('\n☁️  Generating word clouds (may take ~10 seconds)...')

fake_text = ' '.join(df[df['label'] == 'FAKE']['text'].fillna('').values)
wc = WordCloud(width=800, height=350, background_color='white',
               colormap='Reds', max_words=120).generate(fake_text)
plt.figure(figsize=(12, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in FAKE Articles', fontsize=16)
plt.tight_layout()
plt.savefig('data/processed/wordcloud_fake.png', dpi=100)
plt.close()
print('   ✅ Saved → data/processed/wordcloud_fake.png')

real_text = ' '.join(df[df['label'] == 'REAL']['text'].fillna('').values)
wc = WordCloud(width=800, height=350, background_color='white',
               colormap='Greens', max_words=120).generate(real_text)
plt.figure(figsize=(12, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in REAL Articles', fontsize=16)
plt.tight_layout()
plt.savefig('data/processed/wordcloud_real.png', dpi=100)
plt.close()
print('   ✅ Saved → data/processed/wordcloud_real.png')

# ══════════════════════════════════════════════════════════════
# STEP 7 — Final summary
# ══════════════════════════════════════════════════════════════
balance = round(min(real_count, fake_count) / max(real_count, fake_count), 2)

print('\n' + '=' * 50)
print('📊  DATASET SUMMARY')
print('=' * 50)
print(f'Total articles       : {len(df):,}')
print(f'REAL articles        : {real_count:,}')
print(f'FAKE articles        : {fake_count:,}')
print(f'Balance ratio        : {balance}  (1.0 = perfectly balanced)')
print(f'Missing text values  : {df["text"].isnull().sum()}')
print(f'Avg length REAL      : {avg_real:,} characters')
print(f'Avg length FAKE      : {avg_fake:,} characters')
print()
print('Charts saved to  data/processed/')
print()
print('✅  Day 2 complete!')
print('   Next → Day 3: python data/preprocess.py  (clean the data)')
