from flask import Blueprint, jsonify, request, g
from flask_login import login_required, current_user
from loguru import logger

from app.models.group import Group
from app.models.user import User
from app.utils.decorators import permission_required
from app.utils.request_logger import log_user_action

group_bp = Blueprint('group', __name__)

@group_bp.route('/<int:group_id>/')
@login_required
def get_group(group_id):
    group = Group.query.get_or_404(group_id)
    # 记录查看用户组信息行为
    log_user_action(
        "查看用户组信息",
        user=current_user,
        extra_data={
            "用户组ID": group_id,
            "用户组名称": group.name
        }
    )
    return jsonify(group.to_dict())

@group_bp.route('/<int:group_id>/members/')
@login_required
def get_group_members(group_id):
    group = Group.query.get_or_404(group_id)
    # 记录查看用户组成员行为
    log_user_action(
        "查看用户组成员",
        user=current_user,
        extra_data={
            "用户组ID": group_id,
            "用户组名称": group.name
        }
    )
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
    # 记录查看可用用户行为
    log_user_action(
        "查看可用用户（未分配组）",
        user=current_user,
        extra_data={
            "用户组ID": group_id,
            "可用用户数": len(available_users)
        }
    )
    return jsonify({
        'users': [user.to_dict() for user in available_users]
    })

 