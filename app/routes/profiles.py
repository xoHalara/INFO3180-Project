import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app import db, jwt
from app.models import User, Profile, Favourite
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import profile_required

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')

UPLOAD_FOLDER = 'uploads/profile_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.root_path, UPLOAD_FOLDER), filename)

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_profiles():
    limit = request.args.get('limit', default=4, type=int)
    profiles = Profile.query.order_by(Profile.created_at.desc()).limit(limit).all()
    profiles_data = []
    for profile in profiles:
        profile_dict = profile.to_dict()
        profile_dict['name'] = profile.user.name  # Add user's name for frontend
        profiles_data.append(profile_dict)
    return jsonify(profiles_data), 200

@bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_profile():
    current_user_id = get_jwt_identity()
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form
        file = request.files.get('photo')
    else:
        data = request.get_json()
        file = None
    
    if Profile.query.filter_by(user_id_fk=current_user_id).count() >= 3:
        return jsonify({'message': 'Maximum of 3 profiles per user reached'}), 400
    
    required_fields = [
        'description', 'parish', 'biography', 'sex', 'race',
        'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject',
        'political', 'religious', 'family_oriented'
    ]
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required profile fields'}), 400
    
    photo_path = None
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'{uuid.uuid4().hex}.{ext}'
        os.makedirs(os.path.join(current_app.root_path, UPLOAD_FOLDER), exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(os.path.join(current_app.root_path, file_path))
        photo_path = f'/api/profiles/uploads/{filename}'
    
    profile = Profile(
        user_id_fk=current_user_id,
        description=data['description'],
        parish=data['parish'],
        biography=data['biography'],
        sex=data['sex'],
        race=data['race'],
        birth_year=int(data.get('birth_year', 2000)),
        height=float(data['height']),
        fav_cuisine=data['fav_cuisine'],
        fav_colour=data['fav_colour'],
        fav_school_subject=data['fav_school_subject'],
        political=data['political'] in ['true', 'True', '1', 'Yes'],
        religious=data['religious'] in ['true', 'True', '1', 'Yes'],
        family_oriented=data['family_oriented'] in ['true', 'True', '1', 'Yes'],
        photo=photo_path
    )
    profile.check_completeness()
    db.session.add(profile)
    db.session.commit()
    p = profile.to_dict()
    p['name'] = profile.user.name  # Add user's name for frontend
    return jsonify({'message': 'Profile created successfully', 'profile': p}), 201

@bp.route('/<int:profile_id>', methods=['GET'], strict_slashes=False)
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.to_dict()), 200

@bp.route('/<int:user_id>/favourite', methods=['POST'], strict_slashes=False)
@jwt_required()
@profile_required
def add_favorite(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return jsonify({'message': 'Cannot favorite yourself'}), 400
    
    if Favourite.query.filter_by(user_id_fk=current_user_id, fav_user_id_fk=user_id).first():
        return jsonify({'message': 'User already in favorites'}), 400
    
    favourite = Favourite(
        user_id_fk=current_user_id,
        fav_user_id_fk=user_id
    )
    
    db.session.add(favourite)
    db.session.commit()
    
    return jsonify({'message': 'User added to favorites'}), 201

@bp.route('/matches/<int:profile_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_matches(profile_id):
    current_user_id = get_jwt_identity()
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id_fk != current_user_id:
        return jsonify({'message': 'Not authorized to view matches for this profile'}), 403
    
    all_profiles = Profile.query.filter(Profile.user_id_fk != current_user_id).all()
    
    matches = []
    for p in all_profiles:
        age_diff = abs(profile.birth_year - p.birth_year)
        if age_diff > 5:
            continue
        
        height_diff = abs(profile.height - p.height)
        if height_diff < 3 or height_diff > 10:
            continue
        
        matched_fields = 0
        if profile.fav_cuisine == p.fav_cuisine:
            matched_fields += 1
        if profile.fav_colour == p.fav_colour:
            matched_fields += 1
        if profile.fav_school_subject == p.fav_school_subject:
            matched_fields += 1
        if profile.political == p.political:
            matched_fields += 1
        if profile.religious == p.religious:
            matched_fields += 1
        if profile.family_oriented == p.family_oriented:
            matched_fields += 1
            
        if matched_fields >= 3:
            matches.append(p.to_dict())
    
    return jsonify(matches), 200

@bp.route('/<int:profile_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    current_user_id = get_jwt_identity()
    if profile.user_id_fk != current_user_id:
        return jsonify({'message': 'Not authorized to edit this profile'}), 403

    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form
        file = request.files.get('photo')
    else:
        data = request.get_json()
        file = None

    # Update fields if present
    for field in [
        'description', 'parish', 'biography', 'sex', 'race', 'birth_year',
        'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject',
        'political', 'religious', 'family_oriented'
    ]:
        if field in data:
            value = data[field]
            if field in ['height']:
                value = float(value)
            elif field in ['birth_year']:
                value = int(value)
            elif field in ['political', 'religious', 'family_oriented']:
                value = value in ['true', 'True', '1', 'Yes']
            setattr(profile, field, value)

    # Handle photo update
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'{uuid.uuid4().hex}.{ext}'
        os.makedirs(os.path.join(current_app.root_path, UPLOAD_FOLDER), exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(os.path.join(current_app.root_path, file_path))
        profile.photo = f'/api/profiles/uploads/{filename}'

    profile.check_completeness()
    db.session.commit()
    p = profile.to_dict()
    p['name'] = profile.user.name
    return jsonify({'message': 'Profile updated successfully', 'profile': p}), 200