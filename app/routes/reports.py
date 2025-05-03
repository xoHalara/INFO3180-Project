from flask import Blueprint, request, jsonify
from app import db
from app.models import Report, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import profile_required

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
@profile_required
def create_report():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not all(key in data for key in ['reported_user_id', 'reason']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if str(current_user_id) == str(data['reported_user_id']):
        return jsonify({'message': 'Cannot report yourself'}), 400
    
    # Check if reported user exists
    reported_user = User.query.get(data['reported_user_id'])
    if not reported_user:
        return jsonify({'message': 'Reported user not found'}), 404
    
    report = Report(
        reporter_id_fk=current_user_id,
        reported_user_id_fk=data['reported_user_id'],
        reason=data['reason']
    )
    
    db.session.add(report)
    db.session.commit()
    
    return jsonify({'message': 'Report submitted successfully', 'report': report.to_dict()}), 201

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
@profile_required
def get_reports():
    # Get query parameters for sorting
    sort_by = request.args.get('sort_by', 'created_at')  # Default sort by created_at
    order = request.args.get('order', 'desc')  # Default order is descending
    
    # Validate sort_by parameter
    valid_sort_fields = ['created_at', 'reporter_name', 'reported_user_name', 'reason']
    if sort_by not in valid_sort_fields:
        return jsonify({'message': f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}'}), 400
    
    # Build the query
    query = Report.query
    
    # Apply sorting
    if sort_by == 'created_at':
        query = query.order_by(Report.created_at.desc() if order == 'desc' else Report.created_at.asc())
    elif sort_by == 'reporter_name':
        query = query.join(User, Report.reporter_id_fk == User.id)\
            .order_by(User.name.desc() if order == 'desc' else User.name.asc())
    elif sort_by == 'reported_user_name':
        query = query.join(User, Report.reported_user_id_fk == User.id)\
            .order_by(User.name.desc() if order == 'desc' else User.name.asc())
    elif sort_by == 'reason':
        query = query.order_by(Report.reason.desc() if order == 'desc' else Report.reason.asc())
    
    reports = query.all()
    return jsonify([report.to_dict() for report in reports]), 200 