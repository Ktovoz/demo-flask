import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User
from app.models.group import Group

@click.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库"""
    # 创建所有表
    db.create_all()
    
    # 创建默认用户组
    if not Group.query.filter_by(name=Group.SUPER_ADMIN).first():
        super_admin_group = Group(name=Group.SUPER_ADMIN, description='超级管理员组')
        db.session.add(super_admin_group)
    
    if not Group.query.filter_by(name=Group.ADMIN).first():
        admin_group = Group(name=Group.ADMIN, description='管理员组')
        db.session.add(admin_group)
    
    if not Group.query.filter_by(name=Group.USER).first():
        user_group = Group(name=Group.USER, description='普通用户组')
        db.session.add(user_group)
    
    # 创建超级管理员用户
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='admin123',  # 在生产环境中使用更强的密码
            is_active=True
        )
        admin_user.group = Group.query.filter_by(name=Group.SUPER_ADMIN).first()
        db.session.add(admin_user)
    
    db.session.commit()
    click.echo('数据库初始化完成！') 