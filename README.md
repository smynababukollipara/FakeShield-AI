# 🛡️ FakeShield AI

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-orange?logo=scikitlearn)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green)

> **AI-Powered Fake News & Scam Message Detection System**

FakeShield AI is a machine learning-powered web application that analyzes **news articles** and **SMS/WhatsApp messages** to determine whether content is **genuine** or **potentially fake/scam**. The application provides real-time predictions with confidence scores through a modern web interface powered by **Flask** and **Scikit-learn**.

---

# 📑 Table of Contents

- Features
- Project Structure
- Machine Learning Pipeline
- Tech Stack
- Model Performance
- 15-Day Development Timeline
- API Documentation
- Installation
- Running the Project
- Running Tests
- Future Roadmap
- Author
- License

---

# ✨ Features

- ✅ AI-powered Fake News Detection
- ✅ Scam SMS & WhatsApp Detection
- ✅ Real-time Prediction
- ✅ Confidence Score
- ✅ Probability Visualization
- ✅ TXT File Upload
- ✅ Character Counter
- ✅ Detection History (Last 10 Checks)
- ✅ Live Statistics Dashboard
- ✅ Responsive User Interface
- ✅ Flask REST API
- ✅ Health Check Endpoint

---
---

# Screenshots

##  Home Page

![FakeShield AI Home Page](docs/images/home.png)

---

---
# 📁 Project Structure

```text
fake-news-detector/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── predictor.py
│
├── model/
│   ├── train.py
│   ├── evaluate.py
│   └── saved/
│       ├── classifier.pkl
│       └── vectorizer.pkl
│
├── data/
│   ├── preprocess.py
│   ├── scam_examples.py
│   ├── raw/
│   └── processed/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   └── test_predictor.py
│
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🧠 Machine Learning Pipeline

```text
User Input
    │
    ▼
Text Preprocessing
    │
    ▼
TF-IDF Vectorizer
    │
    ▼
PassiveAggressiveClassifier
    │
    ▼
Prediction
    │
    ▼
Confidence Score
    │
    ▼
Display Result
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Backend | Flask |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest |
| Model | PassiveAggressiveClassifier |
| Feature Extraction | TF-IDF Vectorizer |

---

# 📊 Model Performance

| Metric | Naive Bayes | PassiveAggressiveClassifier |
|---------|------------:|----------------------------:|
| Accuracy | 91.95% | **95.74%** |
| Precision | ~0.92 | **0.96** |
| Recall | ~0.92 | **0.96** |
| Dataset Size | 6,335 Articles | 6,335 Articles |

Training Configuration:

- 80/20 Train-Test Split
- TF-IDF (Unigrams + Bigrams)
- Maximum Features: 100,000

---

# 🚀 15-Day Development Timeline

| Day | Progress |
|-----|----------|
| 1 | Folder Structure & Setup |
| 2 | Dataset Collection |
| 3 | Data Cleaning |
| 4 | Naive Bayes Model |
| 5 | Model Evaluation |
| 6 | Flask API |
| 7 | API + Model Integration |
| 8 | Frontend Development |
| 9 | JavaScript Integration |
| 10 | Automated Testing |
| 11 | PassiveAggressiveClassifier Upgrade |
| 12 | Dual Detection Modes |
| 13 | Detection History |
| 14 | Documentation |
| 15 | Final Testing & Deployment |

---

# 🔌 API Documentation

## GET `/health`

Returns the application health status.

**Response**

```json
{
  "status": "healthy"
}
```

## POST `/predict`

**Request**

```json
{
  "text": "Breaking news...",
  "mode": "news"
}
```

**Response**

```json
{
  "prediction": "REAL",
  "confidence": 95.74
}
```

---

# ▶️ Installation

```bash
git clone <repository-url>
cd fake-news-detector

pip install -r requirements.txt
```

(Optional) Retrain the model:

```bash
python model/train.py
```

---

# ▶️ Running the Project

Start the Flask backend:

```bash
python app/main.py
```

Open the frontend in your browser (or via your Node.js proxy if used).

---

# 🧪 Running Tests

```bash
pytest tests/ -v
```

The test suite validates:

- Model loading
- Prediction format
- Empty input
- Long input
- Non-English text
- Confidence score range
- API response format

---

# 🚀 Future Roadmap

- [x] Fake News Detection
- [x] Scam Detection
- [x] TXT Upload
- [ ] PDF Upload
- [ ] DOCX Upload
- [ ] URL Detection
- [ ] Explainable AI
- [ ] Download Prediction Report
- [ ] Dark Mode
- [ ] User Authentication
- [ ] Database Integration

---

# 👨‍💻 Author

**K. Sanjay Babu**

B.Tech – Computer Science & Engineering (AI & ML)

SRM University AP

---

# 📄 License

This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgements

This project uses open-source libraries including Flask, Scikit-learn, Pandas, NumPy, Matplotlib, and Pytest. Thanks to the maintainers of these projects and the public datasets that enabled experimentation and evaluation.
