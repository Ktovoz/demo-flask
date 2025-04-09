from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.group import Group
from app.utils.decorators import permission_required
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>/')
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/create/', methods=['POST'])
@login_required
@permission_required('add_user')
def create_user():
    data = request.get_json()
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'status': 'error', 'message': '用户名已存在'})
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        is_active=data.get('is_active', True)
    )
    
    if data.get('group_id'):
        group = Group.query.get(data.get('group_id'))
        if group:
            user.group = group
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '用户创建成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

@user_bp.route('/<int:user_id>/update/', methods=['POST'])
@login_required
@permission_required('edit_user')
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'status': 'error', 'message': '用户名已存在'})
        user.username = data['username']
    
    if 'email' in data:
        user.email = data['email']
    
    if 'password' in data and data['password']:
        user.password = data['password']
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    if 'group_id' in data:
        group = Group.query.get(data['group_id'])
        if group:
            user.group = group
        else:
            user.group = None
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': '用户更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

@user_bp.route('/<int:user_id>/delete/', methods=['POST'])
@login_required
@permission_required('delete_user')
def delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({'status': 'error', 'message': '不能删除当前登录用户'})
        
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '用户删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

@user_bp.route('/<int:user_id>/change-password/', methods=['POST'])
@login_required
def change_password(user_id):
    if user_id != current_user.id and not current_user.has_permission('edit_user'):
        return jsonify({'status': 'error', 'message': '没有权限'})
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if user_id == current_user.id:
        if not user.verify_password(data.get('old_password')):
            return jsonify({'status': 'error', 'message': '旧密码错误'})
    
    user.password = data.get('new_password')
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
 