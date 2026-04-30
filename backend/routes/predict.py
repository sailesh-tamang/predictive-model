from flask import Blueprint, request, jsonify
from model.model_utils import load_artifacts, prepare_input
import os

bp = Blueprint('predict', __name__)

# Load artifacts at import time (app will import blueprint)
MODEL, SCALER, FEATURES, LABELS = None, None, None, None
try:
    MODEL, SCALER, FEATURES, LABELS = load_artifacts()
except Exception as e:
    # artifacts missing; route will return helpful error
    MODEL = None
    _LOAD_ERR = str(e)


@bp.route('/predict', methods=['POST'])
def predict():
    global MODEL, SCALER, FEATURES
    if MODEL is None:
        return jsonify({
            'error': 'Model artifacts not found. Run backend/model/save_model.py to create model.pkl and scaler.pkl.',
            'details': globals().get('_LOAD_ERR', '')
        }), 500

    payload = request.json or {}
    try:
        X = prepare_input(payload, FEATURES, SCALER)
        proba = MODEL.predict_proba(X)[0]  # order depends on classes_
        classes = list(MODEL.classes_)

        # Map numeric classes back to original labels if mapping exists
        inv_map = None
        if LABELS and 'inv_label_map' in LABELS:
            inv_map = LABELS['inv_label_map']

        proba_map = {}
        for c, p in zip(classes, proba):
            key = str(c)
            if inv_map and str(c) in inv_map:
                key = inv_map[str(c)]
            proba_map[key] = float(p)

        pred_idx = int(proba.argmax())
        pred_class = classes[pred_idx]
        predicted_label = inv_map.get(str(pred_class), str(pred_class)) if inv_map else str(pred_class)
        confidence = float(proba[pred_idx])

        result = {
            'probabilities': proba_map,
            'predicted': predicted_label,
            'confidence': confidence
        }
        return jsonify(result)
    except Exception as ex:
        return jsonify({'error': 'Prediction failed', 'details': str(ex)}), 500
