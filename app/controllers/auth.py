from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.group import Group
from app.forms.auth import LoginForm, RegistrationForm
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            if not user.is_active:
                flash('账号已被禁用')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.strip() or None,
            password=form.password.data
        )
        # 为新用户分配普通用户组
        default_group = Group.query.filter_by(name=Group.USER).first()
        if default_group:
            user.group = default_group
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('注册失败：' + str(e))
            return render_template('register.html', form=form)
    
    # 如果表单验证失败，显示错误信息
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{form[field].label.text}：{error}')
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('您已退出系统')
    return redirect(url_for('auth.login')) 