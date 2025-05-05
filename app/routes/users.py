from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Profile, Favourite
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import profile_required

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@bp.route('/favorites', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favourite.query.filter_by(user_id_fk=current_user_id).all()
    favorite_users = [fav.favorite_user.to_dict() for fav in favorites]
    return jsonify(favorite_users), 200

@bp.route('/<int:user_id>/favourites', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_user_favourites(user_id):
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    valid_sort_fields = ['name', 'parish', 'birth_year']
    if sort_by not in valid_sort_fields:
        return jsonify({'message': f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}'}), 400
    favorites = Favourite.query.filter_by(user_id_fk=user_id).all()
    favorite_users = [fav.favorite_user.to_dict() for fav in favorites]
    reverse = (order == 'desc')
    if sort_by == 'name':
        favorite_users.sort(key=lambda u: (u.get('name') or '').lower(), reverse=reverse)
    elif sort_by == 'parish':
        favorite_users.sort(key=lambda u: (u.get('parish') or '').lower(), reverse=reverse)
    elif sort_by == 'birth_year':
        favorite_users.sort(key=lambda u: u.get('birth_year', 0), reverse=reverse)
    return jsonify(favorite_users), 200

@bp.route('/favourites/<int:n>', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_top_n_favourited(n):
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    valid_sort_fields = ['name', 'parish', 'birth_year', 'favorite_count']
    if sort_by not in valid_sort_fields:
        return jsonify({'message': f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}'}), 400
    if n <= 0:
        return jsonify({'message': 'N must be a positive integer'}), 400
    most_favorited = db.session.query(User, db.func.count(Favourite.id).label('favorite_count'))\
        .join(Favourite, User.id == Favourite.fav_user_id_fk)\
        .group_by(User.id)\
        .all()
    result = []
    for user, count in most_favorited:
        user_dict = user.to_dict()
        user_dict['favorite_count'] = count
        result.append(user_dict)
    reverse = (order == 'desc')
    if sort_by == 'name':
        result.sort(key=lambda u: (u.get('name') or '').lower(), reverse=reverse)
    elif sort_by == 'parish':
        result.sort(key=lambda u: (u.get('parish') or '').lower(), reverse=reverse)
    elif sort_by == 'birth_year':
        result.sort(key=lambda u: u.get('birth_year', 0), reverse=reverse)
    elif sort_by == 'favorite_count':
        result.sort(key=lambda u: u.get('favorite_count', 0), reverse=reverse)
    return jsonify(result[:n]), 200

@bp.route('/most-favorited', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_most_favorited():
    # Get the top 20 most favorited users
    most_favorited = db.session.query(User, db.func.count(Favourite.id).label('favorite_count'))\
        .join(Favourite, User.id == Favourite.fav_user_id_fk)\
        .group_by(User.id)\
        .order_by(db.desc('favorite_count'))\
        .limit(20)\
        .all()
    
    result = []
    for user, count in most_favorited:
        user_dict = user.to_dict()
        user_dict['favorite_count'] = count
        result.append(user_dict)
    
    return jsonify(result), 200

@bp.route('/<int:user_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) != int(user_id):
        return jsonify({'message': 'You can only delete your own account.'}), 403
    user = User.query.get_or_404(user_id)
    # Delete all related favourites (as user and as favourite)
    Favourite.query.filter((Favourite.user_id_fk == user_id) | (Favourite.fav_user_id_fk == user_id)).delete(synchronize_session=False)
    # Delete all related profiles
    Profile.query.filter_by(user_id_fk=user_id).delete(synchronize_session=False)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User and all related data deleted successfully.'}), 200