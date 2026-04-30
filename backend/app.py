import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    from routes.predict import bp as predict_bp
    from routes.images import bp as images_bp
    from routes.shap_explain import bp as shap_bp
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(images_bp, url_prefix='/api')
    app.register_blueprint(shap_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({'message': 'EPL Crowd Impact API', 'status': 'ok'})

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
