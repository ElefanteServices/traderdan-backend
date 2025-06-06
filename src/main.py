import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.crypto import crypto_bp
from src.routes.reports import reports_bp
from src.routes.opportunities import opportunities_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'crypto_trading_dashboard_secret_key_2025'

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(crypto_bp, url_prefix='/api/crypto')
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(opportunities_bp, url_prefix='/api/opportunities')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    return {"status": "healthy", "service": "crypto-trading-api"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

