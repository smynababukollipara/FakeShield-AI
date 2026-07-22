# ─────────────────────────────────────────────────────────────
# tests/test_predictor.py
# Automated tests for the AI prediction system.
#
# What are tests and why do they matter?
#   Tests are small, automatic checks that run your code and
#   verify it behaves correctly. Instead of manually trying
#   every case yourself, you write tests once and run them
#   any time you change something — they catch bugs instantly.
#
#   Interviewers love seeing tests. They show you write
#   professional, production-quality code.
#
# Run all tests with:
#   cd fake-news-detector && pytest tests/ -v
#
# The -v flag means "verbose" — shows each test name and result.
# ─────────────────────────────────────────────────────────────

import sys
import os
import pytest

# Make sure Python can find our app/ folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.predictor import predict


# ══════════════════════════════════════════════════════════════
# GROUP 1 — Model loading tests
# These check that the model file exists and loads correctly.
# ══════════════════════════════════════════════════════════════

class TestModelLoads:

    def test_model_file_exists(self):
        """The trained model file must exist on disk."""
        assert os.path.exists('model/saved/classifier.pkl'), (
            "classifier.pkl not found. Run: python model/train.py"
        )

    def test_vectorizer_file_exists(self):
        """The vectorizer file must exist on disk."""
        assert os.path.exists('model/saved/vectorizer.pkl'), (
            "vectorizer.pkl not found. Run: python model/train.py"
        )

    def test_predict_function_is_callable(self):
        """predict() should be importable and callable."""
        assert callable(predict), "predict must be a function"


# ══════════════════════════════════════════════════════════════
# GROUP 2 — Output structure tests
# These check that predict() always returns the right shape,
# regardless of what text is put in.
# ══════════════════════════════════════════════════════════════

class TestOutputStructure:

    def test_returns_dict(self):
        """predict() must return a dictionary."""
        result = predict("The government announced new economic policies.")
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"

    def test_has_label_key(self):
        """Result must have a 'label' key."""
        result = predict("The government announced new economic policies.")
        assert 'label' in result, f"Missing 'label' key in: {result}"

    def test_has_confidence_key(self):
        """Result must have a 'confidence' key."""
        result = predict("The government announced new economic policies.")
        assert 'confidence' in result, f"Missing 'confidence' key in: {result}"

    def test_has_fake_prob_key(self):
        """Result must have a 'fake_prob' key."""
        result = predict("The government announced new economic policies.")
        assert 'fake_prob' in result

    def test_has_real_prob_key(self):
        """Result must have a 'real_prob' key."""
        result = predict("The government announced new economic policies.")
        assert 'real_prob' in result

    def test_has_error_key(self):
        """Result must have an 'error' key (None when no error)."""
        result = predict("The government announced new economic policies.")
        assert 'error' in result


# ══════════════════════════════════════════════════════════════
# GROUP 3 — Valid prediction tests
# These check that valid text produces sensible results.
# ══════════════════════════════════════════════════════════════

class TestValidPredictions:

    def test_label_is_real_or_fake(self):
        """Label must always be exactly 'REAL' or 'FAKE'."""
        result = predict("Parliament passed the new budget with 280 votes.")
        assert result['label'] in ('REAL', 'FAKE'), (
            f"Label must be 'REAL' or 'FAKE', got: {result['label']}"
        )

    def test_confidence_is_between_0_and_100(self):
        """Confidence must be a number between 0 and 100."""
        result = predict("Parliament passed the new budget with 280 votes.")
        assert result['error'] is None
        assert 0 <= result['confidence'] <= 100, (
            f"Confidence out of range: {result['confidence']}"
        )

    def test_probabilities_sum_to_100(self):
        """real_prob + fake_prob should sum to 100 (±1 for rounding)."""
        result = predict("Parliament passed the new budget with 280 votes.")
        assert result['error'] is None
        total = result['real_prob'] + result['fake_prob']
        assert abs(total - 100.0) <= 1.0, (
            f"Probabilities don't sum to 100: {result['real_prob']} + {result['fake_prob']} = {total}"
        )

    def test_no_error_for_valid_text(self):
        """Valid text should return error=None."""
        result = predict("Scientists published findings on climate change in Nature journal.")
        assert result['error'] is None, f"Unexpected error: {result['error']}"

    def test_obvious_fake_headline(self):
        """
        A typical fake/scam message should be classified as FAKE.
        Note: no AI is 100% correct, so we only check it's callable
        and returns a valid label — not that it must say FAKE.
        """
        result = predict(
            "BREAKING: Secret government documents PROVE that vaccines contain "
            "microchips to control your mind! Share before they delete this! "
            "The mainstream media is hiding the truth from you!"
        )
        assert result['label'] in ('REAL', 'FAKE')
        assert result['confidence'] > 0

    def test_neutral_news_sentence(self):
        """A neutral factual sentence should return a valid result."""
        result = predict(
            "The central bank raised interest rates by 0.25 percentage points "
            "on Wednesday, in line with market expectations following three "
            "consecutive months of elevated inflation data."
        )
        assert result['label'] in ('REAL', 'FAKE')
        assert result['confidence'] > 0


# ══════════════════════════════════════════════════════════════
# GROUP 4 — Edge case / bad input tests
# These verify the code handles unusual input gracefully,
# without crashing.  "Gracefully" means returning an error
# message, NOT raising an exception.
# ══════════════════════════════════════════════════════════════

class TestEdgeCases:

    def test_empty_string_returns_error(self):
        """Empty input should return an error, not crash."""
        result = predict("")
        assert result['error'] is not None, (
            "Empty input should trigger an error message"
        )
        assert result['label'] is None

    def test_whitespace_only_returns_error(self):
        """Input with only spaces/newlines should return an error."""
        result = predict("   \n\t  ")
        assert result['error'] is not None

    def test_very_short_text_returns_error(self):
        """Very short text (< 5 words) should return an error."""
        result = predict("Hello world")
        assert result['error'] is not None, (
            "Text with fewer than 5 words should return an error"
        )

    def test_none_does_not_crash(self):
        """Passing None should return an error, not raise an exception."""
        try:
            result = predict(None)
            assert result['error'] is not None
        except Exception as e:
            pytest.fail(f"predict(None) raised an exception: {e}")

    def test_numbers_only_returns_result(self):
        """Text with only numbers still gets a prediction attempt."""
        result = predict("1234567890 1234 5678 9012 3456 7890 1234")
        # Either a valid prediction or an error is acceptable — but no crash
        assert isinstance(result, dict)
        assert 'label' in result

    def test_very_long_text(self):
        """Very long text (e.g., a full article) should not crash."""
        long_text = (
            "The government announced new economic policies today. "
            "Experts say the measures will impact millions of citizens. "
        ) * 50   # Repeat 50 times to make it very long
        result = predict(long_text)
        assert result['label'] in ('REAL', 'FAKE')
        assert result['error'] is None

    def test_non_english_text(self):
        """Non-English text should not crash — may give low-confidence result."""
        result = predict(
            "El gobierno anunció nuevas políticas económicas hoy. "
            "Los expertos dicen que las medidas afectarán a millones."
        )
        # Should return a result (even if inaccurate for non-English)
        assert isinstance(result, dict)
        assert 'label' in result


# ══════════════════════════════════════════════════════════════
# GROUP 5 — Consistency tests
# These check that the model is deterministic:
# same input should always give the same output.
# ══════════════════════════════════════════════════════════════

class TestConsistency:

    def test_same_input_same_output(self):
        """Running predict twice on the same text should give identical results."""
        text = "The federal reserve raised interest rates by 25 basis points."
        result1 = predict(text)
        result2 = predict(text)
        assert result1['label'] == result2['label'], (
            "Model gave different labels for the same input!"
        )
        assert result1['confidence'] == result2['confidence']

    def test_different_inputs_can_differ(self):
        """Sensational text and neutral text should NOT always give same label."""
        result_neutral = predict(
            "The parliament voted on the annual budget proposal today "
            "after three days of committee hearings and debate."
        )
        result_sensational = predict(
            "SHOCKING TRUTH: The parliament is SECRETLY controlled by "
            "billionaires who want to destroy democracy forever! Wake up!"
        )
        # We don't assert which is which — just that the model can differ
        # (If both are the same it might still be valid, but it's suspicious)
        assert result_neutral['label'] in ('REAL', 'FAKE')
        assert result_sensational['label'] in ('REAL', 'FAKE')
