from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User
from app.models.group import Group

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    users = User.query.all()
    groups = Group.query.all()
    return render_template('index.html',
                         title="用户管理系统",
                         users=users,
                         groups=groups,
                         user=current_user) 