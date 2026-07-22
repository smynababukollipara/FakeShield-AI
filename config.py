# ─────────────────────────────────────────────────────────────
# config.py
# This is the settings file for the whole project.
# Instead of writing the same paths/values in many files,
# we put them here once and import them wherever needed.
# Think of it like a "central control panel".
# ─────────────────────────────────────────────────────────────

import os

# The folder where our trained AI model will be saved
MODEL_DIR = os.path.join("model", "saved")

# The exact file names for our saved model and its vocabulary
MODEL_FILE = os.path.join(MODEL_DIR, "classifier.pkl")
VECTORIZER_FILE = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Path to raw dataset (the CSV file we download from Kaggle)
RAW_DATA_PATH = os.path.join("data", "raw", "dataset.csv")

# Path to cleaned dataset (after we process the raw data)
PROCESSED_DATA_PATH = os.path.join("data", "processed", "clean_data.csv")

# The port number our web server will run on
PORT = 5000

# Set to True while building/testing, False when going live
DEBUG = True
