from flask import Blueprint, request, jsonify
from model.model_utils import load_artifacts, prepare_input
import numpy as np
import io
from flask import send_file
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

bp = Blueprint('shap', __name__)

MODEL, SCALER, FEATURES, LABELS = None, None, None, None
try:
    MODEL, SCALER, FEATURES, LABELS = load_artifacts()
except Exception as e:
    MODEL = None
    _LOAD_ERR = str(e)

try:
    import shap
except Exception:
    shap = None


@bp.route('/shap', methods=['POST'])
def shap_explain():
    if MODEL is None:
        return jsonify({'error': 'Model artifacts not loaded', 'details': globals().get('_LOAD_ERR','')}), 500
    if shap is None:
        return jsonify({'error': 'SHAP library not installed. Install shap in backend environment.'}), 500

    payload = request.json or {}
    try:
        X = prepare_input(payload, FEATURES, SCALER)

        # predict probabilities to determine class for multiclass
        proba = MODEL.predict_proba(X)[0]
        pred_idx = int(np.argmax(proba))

        explainer = shap.Explainer(MODEL)
        expl = explainer(X)

        # handle multi-output shapes: for multiclass, vals is (samples x classes x features) 
        vals = expl.values
        base = expl.base_values
        
        # Extract and flatten properly using numpy operations
        try:
            if isinstance(vals, list):
                # vals is a list of arrays per class
                raw_vals = vals[pred_idx]
                shap_vals = np.asarray(raw_vals).flatten().tolist()
            elif len(vals.shape) == 3:
                # vals is (samples x classes x features) - multiclass output from SHAP
                shap_vals = vals[0, pred_idx, :].flatten().tolist()
            elif len(vals.shape) == 2:
                # vals is (samples x features)
                shap_vals = vals[0, :].flatten().tolist()
            else:
                # fallback
                shap_vals = np.atleast_1d(vals).flatten().tolist()
        except Exception as flatten_err:
            # Last resort: manual conversion
            shap_vals = [float(v) for v in np.asarray(vals).flatten()]
        
        # Convert base_value
        try:
            if isinstance(base, (list, np.ndarray)):
                base_val = float(base[pred_idx]) if hasattr(base, '__len__') and len(base) > pred_idx else float(np.asarray(base).flatten()[0])
            else:
                base_val = float(base)
        except:
            base_val = 0.0

        feature_names = FEATURES
        result = {
            'base_value': base_val,
            'feature_names': feature_names,
            'shap_values': shap_vals,
            'predicted_class_index': pred_idx
        }
        # If label mapping exists, return readable label
        if LABELS and 'inv_label_map' in LABELS:
            inv = LABELS['inv_label_map']
            result['predicted_label'] = inv.get(str(pred_idx), str(pred_idx))

        return jsonify(result)
    except Exception as ex:
        return jsonify({'error': 'SHAP explanation failed', 'details': str(ex)}), 500



@bp.route('/shap_plot', methods=['POST'])
def shap_plot():
    """Generate a static PNG showing SHAP contributions (horizontal bar) for a given input."""
    if MODEL is None:
        return jsonify({'error': 'Model artifacts not loaded', 'details': globals().get('_LOAD_ERR','')}), 500
    if shap is None:
        return jsonify({'error': 'SHAP library not installed. Install shap in backend environment.'}), 500

    payload = request.json or {}
    try:
        X = prepare_input(payload, FEATURES, SCALER)
        explainer = shap.Explainer(MODEL)
        expl = explainer(X)

        vals = expl.values
        # For multiclass, determine predicted class
        proba = MODEL.predict_proba(X)[0]
        pred_idx = int(np.argmax(proba))

        # Extract SHAP values for the predicted class
        if isinstance(vals, list):
            raw_vals = vals[pred_idx]
            shap_values = np.asarray(raw_vals).flatten().tolist()
        elif len(vals.shape) == 3:
            shap_values = vals[0, pred_idx, :].flatten().tolist()
        elif len(vals.shape) == 2:
            shap_values = vals[0, :].flatten().tolist()
        else:
            shap_values = np.atleast_1d(vals).flatten().tolist()

        # Create data tuples manually to avoid DataFrame issues
        features = FEATURES
        data = [(f, float(s), abs(float(s))) for f, s in zip(features, shap_values)]
        # Sort by absolute value (descending)
        data = sorted(data, key=lambda x: x[2], reverse=True)[:30]

        # plot horizontal bar
        fig, ax = plt.subplots(figsize=(8, max(4, len(data)*0.3)))
        names = [d[0] for d in data]
        values = [d[1] for d in data]
        colors = ['green' if v>=0 else 'red' for v in values]
        
        ax.barh(names, values, color=colors)
        ax.set_xlabel('SHAP value')
        ax.set_title('SHAP contributions (top features)')
        ax.invert_yaxis()
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150)
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=False, download_name='shap_plot.png')

    except Exception as ex:
        return jsonify({'error': 'SHAP plot generation failed', 'details': str(ex)}), 500
