from typing import List, Tuple

from loguru import logger

from app.extensions import db
from app.models.group import Group
from app.models.user import User


DEFAULT_GROUPS = [
    (Group.SUPER_ADMIN, '超级管理员组'),
    (Group.ADMIN, '管理员组'),
    (Group.USER, '普通用户组'),
]

DEFAULT_USERS = [
    ('admin', 'admin@example.com', 'admin123', Group.SUPER_ADMIN),
    ('demo', 'demo@example.com', 'demo1234', Group.USER),
]


def ensure_seed_data(commit: bool = True) -> Tuple[List[str], List[str]]:
    """Ensure default groups and demo accounts exist."""
    created_groups: List[str] = []
    created_users: List[str] = []

    for name, description in DEFAULT_GROUPS:
        if not Group.query.filter_by(name=name).first():
            db.session.add(Group(name=name, description=description))
            created_groups.append(name)

    if created_groups:
        logger.info('创建默认用户组: {}', ', '.join(created_groups))
        db.session.flush()

    group_lookup = {group.name: group for group in Group.query.all()}

    for username, email, password, group_name in DEFAULT_USERS:
        if not User.query.filter_by(username=username).first():
            user = User(
                username=username,
                email=email,
                password=password,
                is_active=True,
            )
            group = group_lookup.get(group_name)
            if group:
                user.group = group
            db.session.add(user)
            created_users.append(username)

    if created_users:
        logger.info('创建默认账号: {}', ', '.join(created_users))

    if (created_groups or created_users) and commit:
        db.session.commit()
        logger.success('默认数据已写入数据库')
    elif commit:
        db.session.commit()

    return created_groups, created_users
