from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.group import Group
from app.models.user import User
from app.utils.decorators import permission_required
from app import db

group_bp = Blueprint('group', __name__)

@group_bp.route('/<int:group_id>/')
@login_required
def get_group(group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify(group.to_dict())

@group_bp.route('/<int:group_id>/members/')
@login_required
def get_group_members(group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify({
        'group_name': group.name,
        'members': [user.to_dict() for user in group.users]
    })

@group_bp.route('/available-for-group/<int:group_id>')
@login_required
@permission_required('edit_user')
def get_available_users(group_id):
    # 获取没有分配到任何组的用户
    available_users = User.query.filter(User.group_id.is_(None)).all()
    return jsonify({
        'users': [user.to_dict() for user in available_users]
    })

 