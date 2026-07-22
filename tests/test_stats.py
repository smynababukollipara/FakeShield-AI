# ─────────────────────────────────────────────────────────────
# tests/test_stats.py
# Automated tests for the usage-analytics counter (Day 15).
#
# These tests point the stats module at a temporary JSON file so
# they never touch (or get affected by) the real stats.json used
# by the running app.
#
# Run with:
#   cd fake-news-detector && pytest tests/ -v
# ─────────────────────────────────────────────────────────────

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import stats


@pytest.fixture(autouse=True)
def temp_stats_file(tmp_path, monkeypatch):
    """Redirect STATS_FILE to a throwaway path for every test in this file."""
    fake_path = tmp_path / "stats.json"
    monkeypatch.setattr(stats, 'STATS_FILE', str(fake_path))
    yield


class TestDefaults:

    def test_starts_at_zero(self):
        """With no file on disk yet, all counters should start at 0."""
        result = stats.get_stats()
        assert result['total_checks'] == 0
        assert result['fake_count'] == 0
        assert result['real_count'] == 0
        assert result['fake_pct'] == 0
        assert result['real_pct'] == 0


class TestRecordCheck:

    def test_total_increments(self):
        stats.record_check('FAKE', 'news')
        assert stats.get_stats()['total_checks'] == 1

    def test_fake_count_increments_on_fake_label(self):
        stats.record_check('FAKE', 'news')
        result = stats.get_stats()
        assert result['fake_count'] == 1
        assert result['real_count'] == 0

    def test_real_count_increments_on_real_label(self):
        stats.record_check('REAL', 'news')
        result = stats.get_stats()
        assert result['real_count'] == 1
        assert result['fake_count'] == 0

    def test_mode_counts_track_separately(self):
        stats.record_check('FAKE', 'sms')
        stats.record_check('REAL', 'news')
        result = stats.get_stats()
        assert result['sms_count'] == 1
        assert result['news_count'] == 1

    def test_multiple_checks_accumulate(self):
        for _ in range(3):
            stats.record_check('FAKE', 'news')
        for _ in range(2):
            stats.record_check('REAL', 'news')
        result = stats.get_stats()
        assert result['total_checks'] == 5
        assert result['fake_count'] == 3
        assert result['real_count'] == 2


class TestPercentages:

    def test_percentages_sum_to_100(self):
        stats.record_check('FAKE', 'news')
        stats.record_check('FAKE', 'news')
        stats.record_check('REAL', 'news')
        result = stats.get_stats()
        assert abs((result['fake_pct'] + result['real_pct']) - 100.0) <= 0.1

    def test_all_fake_gives_100_percent_fake(self):
        stats.record_check('FAKE', 'news')
        stats.record_check('FAKE', 'sms')
        result = stats.get_stats()
        assert result['fake_pct'] == 100.0
        assert result['real_pct'] == 0.0


class TestPersistence:

    def test_stats_persist_across_reads(self):
        """A fresh call to get_stats() should see previously recorded checks."""
        stats.record_check('FAKE', 'news')
        first_read = stats.get_stats()
        second_read = stats.get_stats()
        assert first_read['total_checks'] == second_read['total_checks'] == 1

    def test_creates_file_on_disk(self):
        stats.record_check('REAL', 'news')
        assert os.path.exists(stats.STATS_FILE)
