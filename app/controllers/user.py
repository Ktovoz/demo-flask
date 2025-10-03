from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

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
    return jsonify(user.to_dict())


@user_bp.route('/create/', methods=['POST'])
@login_required
@permission_required('add_user')
def create_user_route():
    data = request.get_json() or {}
    result = create_user(data)
    return _build_response(result)


@user_bp.route('/<int:user_id>/update/', methods=['POST'])
@login_required
@permission_required('edit_user')
def update_user_route(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    result = update_user(user, data)
    return _build_response(result)


@user_bp.route('/<int:user_id>/delete/', methods=['POST'])
@login_required
@permission_required('delete_user')
def delete_user_route(user_id):
    if user_id == current_user.id:
        return jsonify({'status': 'error', 'message': '不能删除当前登录用户'})

    user = User.query.get_or_404(user_id)
    result = delete_user(user)
    return _build_response(result)


@user_bp.route('/<int:user_id>/change-password/', methods=['POST'])
@login_required
def change_password_route(user_id):
    if user_id != current_user.id and not current_user.has_permission('edit_user'):
        return jsonify({'status': 'error', 'message': '没有权限'})

    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    new_password = data.get('new_password')
    if not new_password:
        return jsonify({'status': 'error', 'message': '新密码不能为空'})

    if user_id == current_user.id:
        if not user.verify_password(data.get('old_password', '')):
            return jsonify({'status': 'error', 'message': '旧密码错误'})

    result = change_password(user, new_password)
    return _build_response(result)


@user_bp.route('/<int:user_id>/change-group/', methods=['POST'])
@login_required
@permission_required('edit_user')
def change_group_route(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    result = update_user_group(user, data.get('group_id'))
    return _build_response(result)
