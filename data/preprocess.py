# ─────────────────────────────────────────────────────────────
# data/preprocess.py
# Cleans the raw dataset and saves a clean version for training.
#
# Why do we need to clean text?
#   Raw text is messy: "The PRESIDENT said... (Reuters) - Blah!!!"
#   The AI doesn't care about capital letters, punctuation, or
#   common words like "the", "is", "a" — they carry no useful signal.
#   We strip all of that so the AI focuses on what actually matters.
#
# Run from the fake-news-detector/ folder:
#   python data/preprocess.py
# ─────────────────────────────────────────────────────────────

import os
import re
import pandas as pd

# ── Settings ──────────────────────────────────────────────────
RAW_FILE       = 'data/raw/news.csv'
CLEAN_FILE     = 'data/processed/clean_data.csv'

# Stop words: very common English words that carry no meaning
# for fake news detection ("the article said" → same in both classes)
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
    'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
    'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'shall',
    'this', 'that', 'these', 'those', 'it', 'its', 'as', 'not',
    'he', 'she', 'they', 'we', 'i', 'you', 'his', 'her', 'their',
    'our', 'my', 'your', 'said', 'also', 'just', 'about', 'up',
    'out', 'into', 'than', 'then', 'when', 'which', 'who', 'what',
    'all', 'more', 'no', 'so', 'if', 'after', 'before', 'over',
    'new', 'one', 'two', 'can', 'get', 'has', 'us', 'him', 'them'
}


# ══════════════════════════════════════════════════════════════
# The cleaning function — heart of this file
# ══════════════════════════════════════════════════════════════

def clean_text(text: str) -> str:
    """
    Takes one messy string and returns a clean one.

    Steps:
      1. Convert to lowercase         → "Trump" and "trump" become the same
      2. Remove URLs                  → "http://..." adds no meaning
      3. Remove email addresses       → same reason
      4. Remove Reuters-style headers → "(Reuters) - " is boilerplate
      5. Remove punctuation & numbers → "said!!!" → "said"
      6. Collapse extra whitespace    → "  hello  world  " → "hello world"
      7. Remove stop words            → "the president said" → "president"

    Returns an empty string if the input is not a valid string.
    """
    # Guard: if the value is missing (NaN) or not a string, return empty
    if not isinstance(text, str):
        return ''

    # Step 1: Lowercase everything
    text = text.lower()

    # Step 2: Remove URLs  (http://... or https://...)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Step 3: Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Step 4: Remove "(city, agency) -" style news headers
    # Example: "(WASHINGTON) - " or "(Reuters) - "
    text = re.sub(r'\([^)]*\)\s*-\s*', '', text)

    # Step 5: Keep only letters and spaces (remove numbers, punctuation)
    text = re.sub(r'[^a-z\s]', '', text)

    # Step 6: Collapse multiple spaces into one, strip leading/trailing
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 7: Remove stop words
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]

    return ' '.join(words)


# ══════════════════════════════════════════════════════════════
# Main pipeline
# ══════════════════════════════════════════════════════════════

def main():
    os.makedirs('data/processed', exist_ok=True)

    # ── Load raw data ──────────────────────────────────────────
    print('\n📂 Loading raw dataset...')
    df = pd.read_csv(RAW_FILE)
    print(f'   Loaded {len(df):,} rows')

    # ── Drop rows with no text or no label ────────────────────
    before = len(df)
    df = df.dropna(subset=['text', 'label'])
    dropped = before - len(df)
    print(f'   Dropped {dropped} rows with missing text/label')

    # ── Combine title + text for richer signal ─────────────────
    # Titles often carry strong fake/real signals ("BREAKING: ...")
    # Joining them gives the model more to work with
    print('\n🔗 Combining title + text columns...')
    df['combined'] = (
        df['title'].fillna('') + ' ' + df['text'].fillna('')
    )

    # ── Clean the combined text ────────────────────────────────
    print('\n🧹 Cleaning text (this may take ~15 seconds)...')
    df['clean_text'] = df['combined'].apply(clean_text)

    # ── Drop rows where cleaning left empty text ───────────────
    empty_after = (df['clean_text'].str.strip() == '').sum()
    df = df[df['clean_text'].str.strip() != '']
    print(f'   Removed {empty_after} rows that became empty after cleaning')

    # ── Convert labels to numbers ──────────────────────────────
    # Machine learning models work with numbers, not strings
    df['label_num'] = df['label'].map({'REAL': 0, 'FAKE': 1})

    # ── Keep only the columns we need for training ─────────────
    clean_df = df[['clean_text', 'label', 'label_num']].reset_index(drop=True)

    # ── Save the clean dataset ─────────────────────────────────
    clean_df.to_csv(CLEAN_FILE, index=False)
    print(f'\n💾 Saved clean dataset → {CLEAN_FILE}')

    # ── Show a before/after example ────────────────────────────
    print('\n' + '─' * 60)
    print('BEFORE cleaning (first article):')
    print(str(df['combined'].iloc[0])[:300])
    print()
    print('AFTER cleaning:')
    print(str(clean_df['clean_text'].iloc[0])[:300])
    print('─' * 60)

    # ── Final summary ──────────────────────────────────────────
    real_count = (clean_df['label'] == 'REAL').sum()
    fake_count = (clean_df['label'] == 'FAKE').sum()

    print('\n' + '=' * 50)
    print('✅  PREPROCESSING COMPLETE')
    print('=' * 50)
    print(f'Total clean rows  : {len(clean_df):,}')
    print(f'REAL              : {real_count:,}')
    print(f'FAKE              : {fake_count:,}')
    print(f'Saved to          : {CLEAN_FILE}')
    print()
    print('Next → Day 4: python model/train.py  (train the AI!)')


if __name__ == '__main__':
    main()
