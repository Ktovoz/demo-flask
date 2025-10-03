from flask import Blueprint, jsonify, request, g
from flask_login import login_required, current_user
from loguru import logger

from app.models.group import Group
from app.models.user import User
from app.utils.decorators import permission_required
from app.utils.request_logger import log_user_action

group_bp = Blueprint('group', __name__, url_prefix='/groups')


@group_bp.route('/<int:group_id>/')
@login_required
def get_group(group_id):
    """获取指定用户组信息
    
    Args:
        group_id: 用户组ID
        
    Returns:
        JSON: 用户组信息字典
    """
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
    """获取指定用户组的所有成员
    
    Args:
        group_id: 用户组ID
        
    Returns:
        JSON: 包含用户组名称和成员列表的字典
    """
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
    """获取可用于分配到指定用户组的用户（未分配组的用户）
    
    权限要求: edit_user
    Args:
        group_id: 目标用户组ID（用于日志记录）
        
    Returns:
        JSON: 可用用户列表
    """
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

 