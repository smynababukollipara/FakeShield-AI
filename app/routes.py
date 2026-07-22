from flask import Blueprint, request, jsonify
from app.predictor import predict
from app.stats import record_check, get_stats

bp = Blueprint('main', __name__)


@bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Server is running'
    }), 200


@bp.route('/predict', methods=['POST'])
def predict_route():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": 'Request body must be JSON. Example: {"text":"your article"}'
        }), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Missing text field."
        }), 400

    if len(text) > 10000:
        return jsonify({
            "error": "Input is too large."
        }), 400

    mode = data.get("mode", "news")

    if mode not in ["news", "sms"]:
        mode = "news"

    try:
        result = predict(text)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    if result.get("error"):
        return jsonify(result), 400

    record_check(result["label"], mode)

    return jsonify(result), 200


@bp.route('/stats', methods=['GET'])
def stats_route():
    return jsonify(get_stats()), 200