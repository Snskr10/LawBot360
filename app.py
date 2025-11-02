from flask import Flask, render_template, jsonify
from flask_cors import CORS
from config import Config
from models.db import db
import os

# Import routers
from routers import contracts, verify, explain, dashboard, sign, auth, chat

def create_app():
    """Factory function to create Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize JWT
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(contracts.bp, url_prefix='/api/contracts')
    app.register_blueprint(verify.bp, url_prefix='/api/verify')
    app.register_blueprint(explain.bp, url_prefix='/api/explain')
    app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')
    app.register_blueprint(sign.bp, url_prefix='/api/sign')
    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    
    # Create directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['VECTOR_DB_PATH'], exist_ok=True)
    
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/create')
    def create():
        return render_template('create.html')
    
    @app.route('/verify')
    def verify_page():
        return render_template('verify.html')
    
    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')
    
    @app.route('/templates')
    def templates_page():
        return render_template('templates.html')
    
    @app.route('/settings')
    def settings_page():
        return render_template('settings.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


