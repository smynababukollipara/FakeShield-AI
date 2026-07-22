# ─────────────────────────────────────────────────────────────
# app/stats.py
# Tracks simple usage analytics: how many checks have been run,
# and how many were flagged FAKE vs REAL.
#
# Why a JSON file instead of a database?
#   This project has no database — keeping things simple was a
#   deliberate choice (see replit.md). A small JSON file on disk
#   is enough to persist counts across server restarts.
#
# Why a lock?
#   Flask can handle multiple requests "at the same time" using
#   threads. Without a lock, two requests could read the same
#   count, both add 1, and save it back — losing one of the
#   increments. The lock makes sure only one request updates the
#   file at a time.
# ─────────────────────────────────────────────────────────────

import json
import os
import threading

STATS_FILE = os.path.join('data', 'processed', 'stats.json')

_lock = threading.Lock()

_DEFAULT_STATS = {
    'total_checks': 0,
    'fake_count': 0,
    'real_count': 0,
    'news_count': 0,
    'sms_count': 0,
}


def _read_stats() -> dict:
    """Load stats from disk, falling back to zeros if the file is missing/corrupt."""
    try:
        with open(STATS_FILE, 'r') as f:
            data = json.load(f)
            # Make sure every expected key exists (handles older/partial files)
            return {**_DEFAULT_STATS, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULT_STATS)


def _write_stats(stats: dict) -> None:
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def record_check(label: str, mode: str) -> None:
    """
    Call this once per successful prediction to update the counters.

    Parameters
    ----------
    label : str  — "FAKE" or "REAL"
    mode  : str  — "news" or "sms"
    """
    with _lock:
        stats = _read_stats()
        stats['total_checks'] += 1

        if label == 'FAKE':
            stats['fake_count'] += 1
        elif label == 'REAL':
            stats['real_count'] += 1

        if mode == 'sms':
            stats['sms_count'] += 1
        else:
            stats['news_count'] += 1

        _write_stats(stats)


def get_stats() -> dict:
    """
    Return the current counts, plus a couple of handy percentages
    for the frontend to display directly (no extra math needed there).
    """
    with _lock:
        stats = _read_stats()

    total = stats['total_checks']
    fake_pct = round((stats['fake_count'] / total) * 100, 1) if total else 0
    real_pct = round((stats['real_count'] / total) * 100, 1) if total else 0

    return {
        **stats,
        'fake_pct': fake_pct,
        'real_pct': real_pct,
    }
