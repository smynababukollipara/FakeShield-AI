# ─────────────────────────────────────────────────────────────
# model/train.py  (Day 11 — Upgraded Model)
#
# Day 4:  Naive Bayes classifier         → ~91.95% accuracy
# Day 11: PassiveAggressiveClassifier    → typically 95–97%
#
# What is PassiveAggressiveClassifier?
#   It's an "online learning" algorithm originally designed for
#   text classification. The name describes how it works:
#     • PASSIVE : if a prediction is already correct, don't change
#     • AGGRESSIVE : if a prediction is wrong, update strongly
#   This makes it excellent at distinguishing writing styles —
#   exactly what fake vs real news detection needs.
#
# Run from the fake-news-detector/ folder:
#   python model/train.py
# ─────────────────────────────────────────────────────────────

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ── File paths ─────────────────────────────────────────────────
CLEAN_DATA      = 'data/processed/clean_data.csv'
MODEL_DIR       = 'model/saved'
MODEL_FILE      = os.path.join(MODEL_DIR, 'classifier.pkl')
VECTORIZER_FILE = os.path.join(MODEL_DIR, 'vectorizer.pkl')
CM_CHART        = 'data/processed/confusion_matrix.png'


def load_data():
    print('\n📂 Loading clean dataset...')
    df = pd.read_csv(CLEAN_DATA)
    df = df.dropna(subset=['clean_text', 'label_num'])
    df = df[df['clean_text'].str.strip() != '']
    X = df['clean_text'].values
    y = df['label_num'].values
    print(f'   Samples : {len(X):,}  |  REAL: {(y==0).sum():,}  |  FAKE: {(y==1).sum():,}')
    return X, y


def split_data(X, y):
    print('\n✂️  Splitting  →  80% train / 20% test...')
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def vectorize(X_train, X_test):
    print('\n🔢 Vectorizing with TF-IDF (1-grams + 2-grams)...')
    vectorizer = TfidfVectorizer(
        max_features=100_000,   # more features than Day 4 (was 50k)
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2                # ignore words that appear in fewer than 2 articles
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)
    print(f'   Vocabulary : {len(vectorizer.vocabulary_):,} terms')
    return vectorizer, X_train_vec, X_test_vec


def train_and_compare(X_train_vec, X_test_vec, y_train, y_test):
    """Train both algorithms and print a side-by-side comparison."""

    print('\n' + '═' * 55)
    print('  🤖 COMPARING: Naive Bayes  vs  PassiveAggressive')
    print('═' * 55)

    # ── Naive Bayes (Day 4 model) ──────────────────────────────
    nb = MultinomialNB(alpha=0.1)
    nb.fit(X_train_vec, y_train)
    nb_acc = accuracy_score(y_test, nb.predict(X_test_vec))

    # ── Passive Aggressive (Day 11 upgrade) ───────────────────
    pa = PassiveAggressiveClassifier(
        C=0.5,            # regularisation — lower = more conservative
        max_iter=1000,    # maximum training passes
        tol=1e-4,         # stop early if improvement is tiny
        random_state=42
    )
    pa.fit(X_train_vec, y_train)
    pa_acc = accuracy_score(y_test, pa.predict(X_test_vec))

    print(f'\n  Naive Bayes accuracy        : {nb_acc * 100:.2f}%')
    print(f'  PassiveAggressive accuracy  : {pa_acc * 100:.2f}%')
    improvement = (pa_acc - nb_acc) * 100
    arrow = '⬆️ ' if improvement >= 0 else '⬇️ '
    print(f'  Change                      : {arrow}{abs(improvement):.2f} percentage points')

    print('\n  Full report for PassiveAggressive:')
    print(classification_report(y_test, pa.predict(X_test_vec),
                                target_names=['REAL (0)', 'FAKE (1)']))
    return pa, pa_acc


def plot_confusion_matrix(model, X_test_vec, y_test, accuracy):
    y_pred = model.predict(X_test_vec)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted REAL', 'Predicted FAKE'],
                yticklabels=['Actual REAL', 'Actual FAKE'],
                linewidths=0.5)
    plt.title(f'PassiveAggressive  —  Accuracy: {accuracy*100:.1f}%', fontsize=13)
    plt.tight_layout()
    plt.savefig(CM_CHART, dpi=100)
    plt.close()

    print(f'\n  ✅ Correctly called REAL : {tn}')
    print(f'  ✅ Correctly called FAKE : {tp}')
    print(f'  ❌ Real called FAKE (false alarm) : {fp}')
    print(f'  ❌ Fake called REAL (missed fake) : {fn}')
    print(f'\n  Confusion matrix → {CM_CHART}')


def save_model(model, vectorizer):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model,      MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print(f'\n💾 Model saved      → {MODEL_FILE}')
    print(f'💾 Vectorizer saved → {VECTORIZER_FILE}')


def manual_test(model, vectorizer):
    """Quick sanity check with 4 hand-crafted sentences."""
    print('\n' + '─' * 55)
    print('  🧪 Quick sanity check on 4 custom sentences:')
    print('─' * 55)

    import re
    STOP_WORDS = {
        'a','an','the','and','or','but','in','on','at','to','for','of',
        'with','by','from','is','are','was','were','be','been','have',
        'has','had','do','does','did','will','would','could','should',
        'this','that','it','as','not','he','she','they','we','i','you',
        'said','also','just','about','up','all','more','no','so','if',
    }

    def clean(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return ' '.join(w for w in text.split() if w not in STOP_WORDS)

    samples = [
        ("BREAKING: Vaccines cause mind control — government hiding truth!", "FAKE"),
        ("Central bank raised rates 0.25 points, third consecutive increase.", "REAL"),
        ("You won $1,000,000! Send bank details to claim prize now!", "FAKE"),
        ("Parliament approved budget after three days of committee debate.", "REAL"),
    ]

    correct = 0
    for text, expected in samples:
        vec  = vectorizer.transform([clean(text)])
        pred = model.predict(vec)[0]
        label = 'FAKE' if pred == 1 else 'REAL'
        icon  = '✅' if label == expected else '❌'
        print(f'  {icon} "{text[:60]}..."')
        print(f'     Expected: {expected}  |  Got: {label}')
        if label == expected:
            correct += 1

    print(f'\n  Sanity check: {correct}/{len(samples)} correct')


def main():
    print('═' * 55)
    print('🚀  FAKE NEWS DETECTOR — MODEL UPGRADE (Day 11)')
    print('═' * 55)

    X, y                              = load_data()
    X_train, X_test, y_train, y_test  = split_data(X, y)
    vectorizer, X_train_vec, X_test_vec = vectorize(X_train, X_test)
    model, accuracy                   = train_and_compare(X_train_vec, X_test_vec, y_train, y_test)
    plot_confusion_matrix(model, X_test_vec, y_test, accuracy)
    manual_test(model, vectorizer)
    save_model(model, vectorizer)

    print()
    print('═' * 55)
    print(f'✅  UPGRADE COMPLETE — New accuracy: {accuracy * 100:.2f}%')
    print('═' * 55)
    print()
    print('The upgraded model is now saved and will be used')
    print('automatically by the web app — no restart needed.')
    print()
    print('Next → Day 12: add scam SMS detection as a second category')


if __name__ == '__main__':
    main()
