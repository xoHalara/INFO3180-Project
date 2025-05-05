from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS for all routes and origins (for development)
    CORS(app)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the API',
            'endpoints': {
                'auth': '/api/auth',
                'profiles': '/api/profiles',
                'users': '/api/users',
                'search': '/api/search',
                'reports': '/api/reports'
            }
        })
    
    from app.routes import auth, profiles, users, search, reports
    app.register_blueprint(auth.bp)
    app.register_blueprint(profiles.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(reports.bp)
    
    return app

from app.models import User, Profile, Favourite, Report