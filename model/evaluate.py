# ─────────────────────────────────────────────────────────────
# model/evaluate.py
# A deeper look at how well our trained model performs.
#
# train.py told us "91.95% accuracy" — but that single number
# doesn't tell the full story. This file asks:
#   • When it makes a mistake, what kind of mistake is it?
#   • Does it miss more FAKE articles or REAL articles?
#   • What do the articles it got WRONG look like?
#   • Can we test it on our own sentences right now?
#
# Run from the fake-news-detector/ folder:
#   python model/evaluate.py
# ─────────────────────────────────────────────────────────────

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_curve, auc
)

# ── File paths ─────────────────────────────────────────────────
CLEAN_DATA      = 'data/processed/clean_data.csv'
MODEL_FILE      = 'model/saved/classifier.pkl'
VECTORIZER_FILE = 'model/saved/vectorizer.pkl'


# ══════════════════════════════════════════════════════════════
# STEP 1 — Load saved model and recreate the same test split
# ══════════════════════════════════════════════════════════════
# random_state=42 guarantees we get the EXACT same 20% test set
# that was used during training — so the evaluation is fair.

def load_everything():
    print('\n📂 Loading model and data...')
    model      = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    df = pd.read_csv(CLEAN_DATA).dropna(subset=['clean_text', 'label_num'])
    df = df[df['clean_text'].str.strip() != '']

    X = df['clean_text'].values
    y = df['label_num'].values

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_test_vec = vectorizer.transform(X_test)
    y_pred     = model.predict(X_test_vec)

    print(f'   Model loaded     : {MODEL_FILE}')
    print(f'   Test set size    : {len(X_test):,} articles')
    return model, vectorizer, X_test, y_test, X_test_vec, y_pred


# ══════════════════════════════════════════════════════════════
# STEP 2 — Print the classification report
# ══════════════════════════════════════════════════════════════
# Precision : of all articles it labelled FAKE, what % were actually FAKE?
# Recall    : of all actually-FAKE articles, what % did it catch?
# F1-Score  : the balanced average of precision and recall

def print_report(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    print('\n' + '=' * 55)
    print(f'  ACCURACY : {accuracy * 100:.2f}%')
    print('=' * 55)
    print(classification_report(
        y_test, y_pred, target_names=['REAL (0)', 'FAKE (1)']
    ))

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print('  What the confusion matrix means:')
    print(f'  ✅ Correctly called REAL : {tn}')
    print(f'  ✅ Correctly called FAKE : {tp}')
    print(f'  ❌ Real → wrongly called FAKE (false alarm)  : {fp}')
    print(f'  ❌ Fake → wrongly called REAL (missed fake)  : {fn}')
    return accuracy, cm


# ══════════════════════════════════════════════════════════════
# STEP 3 — Plot a visual confusion matrix
# ══════════════════════════════════════════════════════════════

def plot_confusion_matrix(cm, accuracy):
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=['Predicted REAL', 'Predicted FAKE'],
        yticklabels=['Actual REAL', 'Actual FAKE'],
        linewidths=0.5
    )
    plt.title(f'Confusion Matrix  —  Accuracy: {accuracy*100:.1f}%', fontsize=13)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    path = 'data/processed/confusion_matrix.png'
    plt.savefig(path, dpi=100)
    plt.close()
    print(f'\n📊 Confusion matrix saved → {path}')


# ══════════════════════════════════════════════════════════════
# STEP 4 — Look at articles the model got WRONG
# ══════════════════════════════════════════════════════════════
# Studying mistakes is one of the best ways to improve a model.
# We print 3 examples where the model was confidently wrong.

def show_mistakes(model, vectorizer, X_test, y_test, X_test_vec):
    y_pred      = model.predict(X_test_vec)
    y_proba     = model.predict_proba(X_test_vec)  # confidence scores

    mistakes = [
        i for i in range(len(y_test)) if y_pred[i] != y_test[i]
    ]

    print(f'\n🔍 The model made {len(mistakes)} mistakes out of {len(y_test)} articles.')
    print(f'   Showing 3 examples:\n')

    shown = 0
    for i in mistakes[:20]:
        confidence = max(y_proba[i]) * 100
        if confidence > 70:   # only show confident mistakes (more interesting)
            true_label = 'REAL' if y_test[i] == 0 else 'FAKE'
            pred_label = 'REAL' if y_pred[i] == 0 else 'FAKE'
            print(f'  ── Mistake {shown+1} ──────────────────────────────')
            print(f'  Actual label    : {true_label}')
            print(f'  Model predicted : {pred_label}  ({confidence:.0f}% confident)')
            print(f'  Article text    : {X_test[i][:200]}...')
            print()
            shown += 1
            if shown == 3:
                break

    if shown == 0:
        print('  (No highly-confident mistakes found — great model!)')


# ══════════════════════════════════════════════════════════════
# STEP 5 — Test with your own sentences right now
# ══════════════════════════════════════════════════════════════

def manual_test(model, vectorizer):
    print('\n' + '=' * 55)
    print('  🧪 MANUAL TESTS — trying custom sentences')
    print('=' * 55)

    test_sentences = [
        # Likely FAKE — sensational, emotional language
        "BREAKING: Scientists CONFIRM that vaccines cause mind control "
        "and the government is hiding the truth from you!",

        # Likely REAL — neutral, factual reporting style
        "The Federal Reserve raised interest rates by 0.25 percentage "
        "points on Wednesday, citing continued inflation concerns.",

        # Likely FAKE — typical scam message pattern
        "Congratulations! You have won $1,000,000. Click here now "
        "to claim your prize before it expires tonight!",

        # Likely REAL — straightforward news language
        "Parliament approved the new budget after a three-hour debate, "
        "with 287 votes in favour and 201 against.",
    ]

    for sentence in test_sentences:
        vec     = vectorizer.transform([sentence])
        pred    = model.predict(vec)[0]
        proba   = model.predict_proba(vec)[0]
        label   = 'FAKE 🔴' if pred == 1 else 'REAL 🟢'
        conf    = max(proba) * 100
        print(f'\n  Input   : "{sentence[:80]}..."')
        print(f'  Result  : {label}  ({conf:.1f}% confidence)')


# ══════════════════════════════════════════════════════════════
# Run everything
# ══════════════════════════════════════════════════════════════

def main():
    print('=' * 55)
    print('🔬  FAKE NEWS DETECTOR — DEEP EVALUATION')
    print('=' * 55)

    model, vectorizer, X_test, y_test, X_test_vec, y_pred = load_everything()
    accuracy, cm = print_report(y_test, y_pred)
    plot_confusion_matrix(cm, accuracy)
    show_mistakes(model, vectorizer, X_test, y_test, X_test_vec)
    manual_test(model, vectorizer)

    print('\n' + '=' * 55)
    print('✅  EVALUATION COMPLETE')
    print('=' * 55)
    print('\nNext → Day 6: build the Flask web server (app/main.py)')


if __name__ == '__main__':
    main()
