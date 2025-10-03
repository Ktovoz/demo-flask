from dataclasses import dataclass
from typing import Optional

from loguru import logger

from app.extensions import db
from app.models.group import Group
from app.models.user import User


@dataclass
class AuthResult:
    success: bool
    user: Optional[User] = None
    message: str = ''
    status: str = 'ok'


def authenticate_user(username: str, password: str) -> AuthResult:
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        logger.warning('用户 {} 登录失败: 凭证无效', username)
        return AuthResult(success=False, message='用户名或密码错误', status='invalid')

    if not user.is_active:
        logger.warning('禁用账号尝试登录: {}', username)
        return AuthResult(success=False, user=user, message='账号已被禁用', status='disabled')

    logger.info('用户 {} 登录成功', username)
    return AuthResult(success=True, user=user)


def register_user(username: str, email: Optional[str], password: str) -> AuthResult:
    user = User(
        username=username,
        email=(email or '').strip() or None,
        password=password,
    )

    default_group = Group.query.filter_by(name=Group.USER).first()
    if default_group:
        user.group = default_group

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('注册失败: %s', username)
        return AuthResult(success=False, user=None, message=str(exc), status='error')

    logger.info('新用户注册成功: %s', username)
    return AuthResult(success=True, user=user)
