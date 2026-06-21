from flask import Blueprint, jsonify, send_from_directory, abort
import os

bp = Blueprint('images', __name__)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


def _image_files():
    return sorted(
        fname for fname in os.listdir(ROOT)
        if os.path.isfile(os.path.join(ROOT, fname)) and fname.lower().endswith(IMAGE_EXTS)
    )


@bp.route('/images/list', methods=['GET'])
def list_images():
    return jsonify({'images': _image_files()})


@bp.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    if filename not in _image_files():
        abort(404)

    return send_from_directory(
        ROOT,
        filename,
        conditional=True,
        max_age=604800,
    )