# Resume & Interview Prep — Fake News & Scam Detector

## 📌 Resume bullet points (pick 2–3, tailor to the job)

**Short version (1 line):**
> Built an AI-powered fake news and scam message detector (Python, Flask, scikit-learn) achieving 95.7% accuracy on 6,300+ articles, with a full-stack web interface and 24 automated tests.

**Full version (3 bullets, for a Projects section):**

- Developed a full-stack machine learning web application that classifies news articles and SMS/WhatsApp messages as real or fake/scam, using TF-IDF vectorization and a PassiveAggressiveClassifier trained on 6,335 labeled articles, achieving **95.74% test accuracy** (up from a 91.95% Naive Bayes baseline).
- Designed and built a REST API in Flask serving real-time predictions with confidence scores, connected to a responsive HTML/CSS/JavaScript frontend via a Node.js/Express proxy, including a dual-mode UI (news vs. scam messages) and a persistent check-history feature.
- Wrote a 24-test automated test suite with pytest covering model behavior, edge cases, and API contracts, ensuring reliability before deployment.

## 🗣 Interview talking points

**"Walk me through this project."**
> "I built an end-to-end text classification system. I started by sourcing a labeled dataset of ~6,300 news articles, cleaned and vectorized the text with TF-IDF, and trained a baseline Naive Bayes model that got ~92% accuracy. I then compared it against a PassiveAggressiveClassifier — an online learning algorithm well suited to text — which pushed accuracy to 95.7%. I wrapped the model in a Flask API, built a frontend that lets users check either news articles or SMS scam messages, and covered the whole thing with automated tests."

**"Why PassiveAggressiveClassifier instead of a neural network / BERT?"**
> "I considered a transformer model, but PassiveAggressiveClassifier gave a large accuracy jump (+3.8 points) over Naive Bayes without needing GPU resources or heavy dependencies like PyTorch. For a project of this size, it's a strong practical trade-off — fast to train, fast to serve, and easy to explain in an interview. If I were scaling this to production with more data and infrastructure, a fine-tuned transformer (e.g. DistilBERT) would likely raise accuracy further."

**"How did you validate the model isn't overfitting?"**
> "I used an 80/20 train/test split with stratified sampling to keep the class balance even, evaluated with a confusion matrix and full precision/recall/F1 report, and ran manual sanity checks with hand-written sentences the model had never seen — including one it got wrong, which I intentionally kept in my evaluation script to show honest limitations rather than cherry-picked results."

**"What was the hardest part?"**
> "Two things: first, getting the TF-IDF feature space right — too few features underfit, too many slowed things down for little gain, so I tuned `max_features` and used both unigrams and bigrams. Second, making the two detection modes (news vs. SMS) feel like a coherent product rather than two separate tools — that meant adapting the explanation text, verdict labels, and examples per mode instead of just reusing one generic UI."

**"What would you improve with more time?"**
> "Three things: swap in a transformer model for higher accuracy, add real user-reported feedback so the model can be retrained on live data, and move persistent history from the browser's localStorage into a real database with user accounts."

## 🔑 Key numbers to remember

| Stat | Value |
|---|---|
| Dataset size | 6,335 news articles |
| Class balance | ~50/50 real vs fake |
| Baseline model | Naive Bayes — 91.95% accuracy |
| Final model | PassiveAggressiveClassifier — **95.74% accuracy** |
| Test coverage | 24 automated pytest tests, all passing |
| Vectorizer | TF-IDF, unigrams + bigrams, 100,000 max features |
| Modes supported | News articles, SMS/WhatsApp scam messages |

## 🧠 Skills this project demonstrates

- Machine learning fundamentals (feature extraction, train/test splits, model comparison, evaluation metrics)
- REST API design (Flask)
- Full-stack integration (Python backend + JS frontend + Node.js proxy)
- Automated testing (pytest)
- Product thinking (dual-mode UX, history feature, honest model limitations)
