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

def create_app(config=None):
    """Application factory with explicit configuration support"""
    # Load environment variables
    load_dotenv()
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configure application
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-secret-key'),
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'jwt-secret-key'),
        'CORS_HEADERS': 'Content-Type'
    })
    
    # Apply additional configuration if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS for all API routes
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    """Register all application blueprints with proper URL prefixes"""
    from src.routes.user import user_bp
    from src.routes.job import job_bp
    from src.routes.candidate import candidate_bp
    from src.routes.application import application_bp
    from src.routes.agency import agency_bp
    from src.routes.matching import matching_bp
    from src.routes.communication import communication_bp
    from src.routes.overview import overview_bp
    
    blueprints = [
        (user_bp, '/api'),
        (job_bp, '/api'),
        (candidate_bp, '/api'),
        (application_bp, '/api'),
        (agency_bp, '/api'),
        (matching_bp, '/api'),
        (communication_bp, '/api'),
        (overview_bp, '/api/overview')  # Special prefix for overview
    ]
    
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

def register_error_handlers(app):
    """Register global error handlers with JSON responses"""
    from flask import jsonify
    from werkzeug.exceptions import HTTPException
    import traceback
    
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        """Return JSON instead of HTML for HTTP errors"""
        response = {
            "success": False,
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }
        return jsonify(response), e.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """Log unexpected errors and return clean response"""
        app.logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }), 500

# Import all models for Flask-Migrate to detect
from src.models.user import User
from src.models.job import Job
from src.models.candidate import Candidate
from src.models.application import Application
from src.models.communication import CommunicationLog
from src.models.agency import RecruitmentAgency, Commission
