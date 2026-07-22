
import sys
import os

# Make sure Python can find our app/ and model/ folders
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory
from flask_cors import CORS
from app.routes import bp

# ── Folder paths ───────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# ── Create the Flask app ───────────────────────────────────────
# static_folder points Flask to our frontend/ folder so it can
# serve style.css and script.js automatically at /static/<filename>
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path='/static'
)
CORS(app)

# ── Register the API routes (/predict, /health) ────────────────
app.register_blueprint(bp)

# ── Serve the HTML page at the root URL "/" ────────────────────
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

# ── Start the server ───────────────────────────────────────────
if __name__ == '__main__':
    PORT  = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

    print()
    print('=' * 50)
    print('  Fake News Detector — starting...')
    print(f'    Open in browser: http://localhost:{PORT}')
    print()
    print('  API endpoints:')
    print(f'    GET  http://localhost:{PORT}/health')
    print(f'    POST http://localhost:{PORT}/predict')
    print('=' * 50)
    print()

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
