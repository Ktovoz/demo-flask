from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from loguru import logger

from app.models.user import User
from app.models.group import Group
from app.forms.auth import LoginForm, RegistrationForm
from app import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.debug('已登录用户 {} 访问登录页，重定向至首页', current_user.username)
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(form.password.data):
            if not user.is_active:
                flash('账号已被禁用')
                logger.warning('禁用账号尝试登录: {}', username)
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            logger.info('用户 {} 登录成功', username)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('用户名或密码错误')
        logger.warning('用户 {} 登录失败: 凭证无效', username)
    elif form.errors:
        logger.debug('登录表单校验失败: {}', form.errors)
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.debug('已登录用户 {} 访问注册页，重定向至首页', current_user.username)
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=(form.email.data or '').strip() or None,
            password=form.password.data
        )
        default_group = Group.query.filter_by(name=Group.USER).first()
        if default_group:
            user.group = default_group

        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录')
            logger.info('新用户注册成功: {}', user.username)
            return redirect(url_for('auth.login'))
        except Exception as exc:
            db.session.rollback()
            logger.exception('注册失败: %s', form.username.data)
            flash('注册失败: ' + str(exc))
            return render_template('register.html', form=form)

    if form.errors:
        logger.debug('注册表单校验错误: %s', form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}：{error}")

    return render_template('register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logger.info('用户 {} 退出系统', current_user.username)
    logout_user()
    flash('您已退出系统')
    return redirect(url_for('auth.login'))
