from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from app.extensions import db
from app.models.group import Group
from app.models.user import User


@dataclass
class ServiceResponse:
    success: bool
    message: str
    data: Optional[Any] = None


def _load_group(group_id: Optional[int]) -> Optional[Group]:
    if not group_id:
        return None
    return Group.query.get(group_id)


def create_user(payload: Dict[str, Any]) -> ServiceResponse:
    username = (payload.get('username') or '').strip()
    if not username:
        return ServiceResponse(False, '用户名不能为空')

    if User.query.filter_by(username=username).first():
        return ServiceResponse(False, '用户名已存在')

    user = User(
        username=username,
        email=payload.get('email'),
        password=payload.get('password'),
        is_active=payload.get('is_active', True)
    )

    group = _load_group(payload.get('group_id'))
    if group:
        user.group = group

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('创建用户失败: %s', username)
        return ServiceResponse(False, str(exc))

    logger.info('创建用户成功: %s', username)
    return ServiceResponse(True, '用户创建成功', data=user.to_dict())


def update_user(user: User, payload: Dict[str, Any]) -> ServiceResponse:
    username = payload.get('username')
    if username and username != user.username:
        if User.query.filter_by(username=username).first():
            return ServiceResponse(False, '用户名已存在')
        user.username = username

    if 'email' in payload:
        user.email = payload['email']

    if payload.get('password'):
        user.password = payload['password']

    if 'is_active' in payload:
        user.is_active = payload['is_active']

    if 'group_id' in payload:
        group = _load_group(payload.get('group_id'))
        user.group = group

    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('更新用户失败: %s', user.username)
        return ServiceResponse(False, str(exc))

    logger.info('更新用户成功: %s', user.username)
    return ServiceResponse(True, '用户更新成功', data=user.to_dict())


def delete_user(user: User) -> ServiceResponse:
    username = user.username
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('删除用户失败: %s', username)
        return ServiceResponse(False, str(exc))

    logger.info('删除用户成功: %s', username)
    return ServiceResponse(True, '用户删除成功')


def change_password(user: User, new_password: str) -> ServiceResponse:
    user.password = new_password
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('修改密码失败: %s', user.username)
        return ServiceResponse(False, str(exc))

    logger.info('修改密码成功: %s', user.username)
    return ServiceResponse(True, '密码修改成功')
