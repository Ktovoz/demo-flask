from flask import Blueprint, render_template, g
from flask_login import current_user, login_required
from loguru import logger

from app.models.group import Group
from app.models.user import User
from app.utils.request_logger import log_user_action


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    users = User.query.all()
    groups = Group.query.all()
    users_data = [user.to_dict() for user in users]
    groups_data = [group.to_dict() for group in groups]

    # 记录用户访问首页的行为
    log_user_action(
        "访问首页",
        user=current_user,
        extra_data={
            "用户数": len(users),
            "用户组数": len(groups)
        }
    )

    return render_template(
        'index.html',
        title='用户管理系统',
        users=users,
        groups=groups,
        users_data=users_data,
        groups_data=groups_data,
        user=current_user,
    )
