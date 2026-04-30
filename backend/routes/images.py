from flask import Blueprint, jsonify, send_from_directory, current_app
import os

bp = Blueprint('images', __name__)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif')


@bp.route('/images/list', methods=['GET'])
def list_images():
    # scan repository root for image files produced by research
    imgs = []
    for fname in os.listdir(ROOT):
        if fname.lower().endswith(IMAGE_EXTS):
            imgs.append(fname)
    return jsonify({'images': imgs})


@bp.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    # serve files from repository root (where your PNGs live)
    safe_dir = ROOT
    return send_from_directory(safe_dir, filename)
