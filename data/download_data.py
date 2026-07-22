# ─────────────────────────────────────────────────────────────
# data/download_data.py
# Downloads a real fake news dataset automatically.
# Run this file from the fake-news-detector/ folder:
#   python data/download_data.py
# ─────────────────────────────────────────────────────────────

import os
import urllib.request   # built into Python — no install needed

# ── Where to save the downloaded file ─────────────────────────
RAW_FOLDER = os.path.join("data", "raw")
OUTPUT_FILE = os.path.join(RAW_FOLDER, "news.csv")

# ── The public dataset URL ─────────────────────────────────────
# Source: George McIntire's fake news dataset (GitHub, public domain)
# ~7,000 articles — columns: title, text, label (REAL / FAKE)
DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "lutzhamel/fake-news/master/data/fake_or_real_news.csv"
)

def download():
    # Create the folder if it doesn't exist yet
    os.makedirs(RAW_FOLDER, exist_ok=True)

    if os.path.exists(OUTPUT_FILE):
        print(f"✅ Dataset already exists at: {OUTPUT_FILE}")
        print("   Delete it and re-run if you want a fresh download.")
        return

    print("⬇️  Downloading dataset...")
    print(f"   URL : {DATASET_URL}")
    print(f"   Saving to : {OUTPUT_FILE}")
    print("   (This may take 10–30 seconds depending on your connection)")

    try:
        urllib.request.urlretrieve(DATASET_URL, OUTPUT_FILE)
        print()
        print("✅ Download complete!")

        # Quick check — show file size and first line
        size_kb = os.path.getsize(OUTPUT_FILE) // 1024
        print(f"   File size : {size_kb} KB")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            print(f"   First line: {f.readline().strip()}")

    except Exception as e:
        print(f"❌ Download failed: {e}")
        print()
        print("   Try this manual fix:")
        print("   1. Open this URL in your browser:")
        print(f"      {DATASET_URL}")
        print(f"   2. Save the page as:  {OUTPUT_FILE}")

if __name__ == "__main__":
    download()
