from dataclasses import dataclass
from typing import Any, Dict, Optional

from loguru import logger

from app.extensions import db
from app.models.group import Group
from app.models.user import User


@dataclass
class ServiceResponse:
    """服务层响应数据类
    
    Attributes:
        success: 操作是否成功
        message: 响应消息
        data: 响应数据（可选）
    """
    success: bool
    message: str
    data: Optional[Any] = None


def _load_group(group_id: Optional[int]) -> Optional[Group]:
    """根据ID加载用户组
    
    Args:
        group_id: 用户组ID
        
    Returns:
        Group: 用户组对象，如果未找到则返回None
    """
    if not group_id:
        return None
    return Group.query.get(group_id)


def _normalise_group_id(value: Optional[Any]) -> Optional[int]:
    """规范化用户组ID值
    
    Args:
        value: 待处理的值
        
    Returns:
        int: 规范化后的用户组ID，如果无效则返回None
    """
    if value in (None, '', 'null'):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_bool(value: Any, default: bool = True) -> bool:
    """将值转换为布尔类型
    
    Args:
        value: 待转换的值
        default: 默认值
        
    Returns:
        bool: 转换后的布尔值
    """
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


def create_user(payload: Dict[str, Any]) -> ServiceResponse:
    """创建新用户
    
    Args:
        payload: 包含用户信息的字典
        
    Returns:
        ServiceResponse: 服务响应对象
    """
    username = (payload.get('username') or '').strip()
    if not username:
        return ServiceResponse(False, '用户名不能为空')

    if User.query.filter_by(username=username).first():
        return ServiceResponse(False, '用户名已存在')

    user = User(
        username=username,
        email=(payload.get('email') or '').strip() or None,
        password=payload.get('password'),
        is_active=_to_bool(payload.get('is_active'), True)
    )

    group = _load_group(_normalise_group_id(payload.get('group_id')))
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
    """更新用户信息
    
    Args:
        user: 要更新的用户对象
        payload: 包含更新信息的字典
        
    Returns:
        ServiceResponse: 服务响应对象
    """
    username = payload.get('username')
    if username and username != user.username:
        if User.query.filter_by(username=username).first():
            return ServiceResponse(False, '用户名已存在')
        user.username = username

    if 'email' in payload:
        user.email = (payload.get('email') or '').strip() or None

    if payload.get('password'):
        user.password = payload['password']

    if 'is_active' in payload:
        user.is_active = _to_bool(payload.get('is_active'), user.is_active)

    if 'group_id' in payload:
        group = _load_group(_normalise_group_id(payload.get('group_id')))
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
    """删除用户
    
    Args:
        user: 要删除的用户对象
        
    Returns:
        ServiceResponse: 服务响应对象
    """
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
    """修改用户密码
    
    Args:
        user: 要修改密码的用户对象
        new_password: 新密码
        
    Returns:
        ServiceResponse: 服务响应对象
    """
    user.password = new_password
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('修改密码失败: %s', user.username)
        return ServiceResponse(False, str(exc))

    logger.info('修改密码成功: %s', user.username)
    return ServiceResponse(True, '密码修改成功')


def update_user_group(user: User, group_id: Optional[Any]) -> ServiceResponse:
    """更新用户组
    
    Args:
        user: 要更新的用户对象
        group_id: 新的用户组ID
        
    Returns:
        ServiceResponse: 服务响应对象
    """
    group = _load_group(_normalise_group_id(group_id))
    user.group = group
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('调整用户组失败: %s', user.username)
        return ServiceResponse(False, str(exc))
    return ServiceResponse(True, '操作成功', data=user.to_dict())
