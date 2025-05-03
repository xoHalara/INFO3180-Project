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
    favorites = Favourite.query.filter_by(user_id_fk=user_id).all()
    favorite_users = [fav.favorite_user.to_dict() for fav in favorites]
    return jsonify(favorite_users), 200

@bp.route('/favourites/<int:n>', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_top_n_favourited(n):
    if n <= 0:
        return jsonify({'message': 'N must be a positive integer'}), 400
    most_favorited = db.session.query(User, db.func.count(Favourite.id).label('favorite_count'))\
        .join(Favourite, User.id == Favourite.fav_user_id_fk)\
        .group_by(User.id)\
        .order_by(db.desc('favorite_count'))\
        .limit(n)\
        .all()
    result = []
    for user, count in most_favorited:
        user_dict = user.to_dict()
        user_dict['favorite_count'] = count
        result.append(user_dict)
    return jsonify(result), 200

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