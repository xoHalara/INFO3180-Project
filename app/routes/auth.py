from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db, jwt
from app.models import User, Profile
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['username', 'password', 'name', 'email']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['username', 'password']):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Check if user has at least one fully completed profile
    has_profile = user.has_complete_profile()

    access_token = create_access_token(identity=str(user.id), additional_claims={'has_profile': has_profile})
    return jsonify({
        'access_token': access_token,
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'has_profile': has_profile
    }), 200

@bp.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    return jsonify({'message': 'Successfully logged out'}), 200