# backend/src/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory function"""
    # Load environment variables
    load_dotenv()
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configure application
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-secret-key'),
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/recruitment'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'CORS_HEADERS': 'Content-Type'
    })
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('ALLOWED_ORIGINS', '*').split(',')
        }
    })
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create tables (for development)
    with app.app_context():
        db.create_all()
    
    return app

def register_blueprints(app):
    """Register all application blueprints"""
    from src.routes.auth import auth_bp
    from src.routes.jobs import jobs_bp
    from src.routes.candidates import candidates_bp
    from src.routes.applications import applications_bp
    from src.routes.overview import overview_bp
    from src.routes.communications import communications_bp
    
    blueprints = [
        (auth_bp, '/api/auth'),
        (jobs_bp, '/api/jobs'),
        (candidates_bp, '/api/candidates'),
        (applications_bp, '/api/applications'),
        (overview_bp, '/api/overview'),
        (communications_bp, '/api/communications')
    ]
    
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

def register_error_handlers(app):
    """Register global error handlers"""
    from flask import jsonify
    from werkzeug.exceptions import HTTPException
    
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        """Handle HTTP exceptions"""
        return jsonify({
            'error': e.name,
            'message': e.description,
            'status_code': e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """Handle unexpected exceptions"""
        app.logger.error(f'Unexpected error: {str(e)}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

# Import models for Flask-Migrate
from src.models import (  # noqa
    user, job, candidate, 
    application, communication, 
    agency, commission
)
