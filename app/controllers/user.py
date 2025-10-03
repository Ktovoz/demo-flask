from flask import Blueprint, jsonify, request, g
from flask_login import current_user, login_required
from loguru import logger

from app.models.user import User
from app.services.user_service import (
    ServiceResponse,
    change_password,
    create_user,
    delete_user,
    update_user,
    update_user_group,
)
from app.utils.decorators import permission_required
from app.utils.request_logger import log_user_action


user_bp = Blueprint('user', __name__)


def _build_response(result: ServiceResponse):
    payload = {
        'status': 'success' if result.success else 'error',
        'message': result.message,
    }
    if result.data is not None:
        payload['data'] = result.data
    return jsonify(payload)


@user_bp.route('/<int:user_id>/')
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    # 记录查看用户信息行为
    log_user_action(
        "查看用户信息",
        user=current_user,
        extra_data={
            "查看用户ID": user_id,
            "查看用户名": user.username
        }
    )
    return jsonify(user.to_dict())


@user_bp.route('/create/', methods=['POST'])
@login_required
@permission_required('add_user')
def create_user_route():
    data = request.get_json() or {}
    result = create_user(data)
    
    # 记录创建用户行为
    if result.success:
        log_user_action(
            "创建用户成功",
            user=current_user,
            extra_data={
                "新用户ID": result.data.get('id') if result.data else 'Unknown',
                "新用户名": data.get('username', 'Unknown')
            }
        )
    else:
        log_user_action(
            "创建用户失败",
            user=current_user,
            extra_data={
                "用户名": data.get('username', 'Unknown'),
                "原因": result.message
            }
        )
    
    return _build_response(result)


@user_bp.route('/<int:user_id>/update/', methods=['POST'])
@login_required
@permission_required('edit_user')
def update_user_route(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    result = update_user(user, data)
    
    # 记录更新用户行为
    if result.success:
        log_user_action(
            "更新用户成功",
            user=current_user,
            extra_data={
                "更新用户ID": user_id,
                "更新用户名": user.username
            }
        )
    else:
        log_user_action(
            "更新用户失败",
            user=current_user,
            extra_data={
                "更新用户ID": user_id,
                "更新用户名": user.username,
                "原因": result.message
            }
        )
    
    return _build_response(result)


@user_bp.route('/<int:user_id>/delete/', methods=['POST'])
@login_required
@permission_required('delete_user')
def delete_user_route(user_id):
    if user_id == current_user.id:
        log_user_action(
            "尝试删除自己账户",
            user=current_user,
            extra_data={
                "用户ID": user_id
            }
        )
        return jsonify({'status': 'error', 'message': '不能删除当前登录用户'})

    user = User.query.get_or_404(user_id)
    result = delete_user(user)
    
    # 记录删除用户行为
    if result.success:
        log_user_action(
            "删除用户成功",
            user=current_user,
            extra_data={
                "删除用户ID": user_id,
                "删除用户名": user.username
            }
        )
    else:
        log_user_action(
            "删除用户失败",
            user=current_user,
            extra_data={
                "删除用户ID": user_id,
                "删除用户名": user.username,
                "原因": result.message
            }
        )
    
    return _build_response(result)


@user_bp.route('/<int:user_id>/change-password/', methods=['POST'])
@login_required
def change_password_route(user_id):
    if user_id != current_user.id and not current_user.has_permission('edit_user'):
        log_user_action(
            "尝试修改他人密码（无权限）",
            user=current_user,
            extra_data={
                "目标用户ID": user_id
            }
        )
        return jsonify({'status': 'error', 'message': '没有权限'})

    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    new_password = data.get('new_password')
    if not new_password:
        log_user_action(
            "修改密码失败（新密码为空）",
            user=current_user,
            extra_data={
                "目标用户ID": user_id,
                "目标用户名": user.username
            }
        )
        return jsonify({'status': 'error', 'message': '新密码不能为空'})

    if user_id == current_user.id:
        if not user.verify_password(data.get('old_password', '')):
            log_user_action(
                "修改密码失败（旧密码错误）",
                user=current_user,
                extra_data={
                    "用户ID": user_id,
                    "用户名": user.username
                }
            )
            return jsonify({'status': 'error', 'message': '旧密码错误'})

    result = change_password(user, new_password)
    
    # 记录修改密码行为
    if result.success:
        log_user_action(
            "修改密码成功",
            user=current_user,
            extra_data={
                "目标用户ID": user_id,
                "目标用户名": user.username
            }
        )
    else:
        log_user_action(
            "修改密码失败",
            user=current_user,
            extra_data={
                "目标用户ID": user_id,
                "目标用户名": user.username,
                "原因": result.message
            }
        )
    
    return _build_response(result)


@user_bp.route('/<int:user_id>/change-group/', methods=['POST'])
@login_required
@permission_required('edit_user')
def change_group_route(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    result = update_user_group(user, data.get('group_id'))
    
    # 记录修改用户组行为
    if result.success:
        log_user_action(
            "修改用户组成功",
            user=current_user,
            extra_data={
                "用户ID": user_id,
                "用户名": user.username,
                "新组ID": data.get('group_id', 'None')
            }
        )
    else:
        log_user_action(
            "修改用户组失败",
            user=current_user,
            extra_data={
                "用户ID": user_id,
                "用户名": user.username,
                "新组ID": data.get('group_id', 'None'),
                "原因": result.message
            }
        )
    
    return _build_response(result)
