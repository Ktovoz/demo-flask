from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger

from app.forms.auth import LoginForm, RegistrationForm
from app.services.auth_service import authenticate_user, register_user


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.debug('已登录用户 %s 访问登录页，重定向至首页', current_user.username)
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        result = authenticate_user(form.username.data, form.password.data)
        if result.success and result.user:
            login_user(result.user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)

        if result.status == 'disabled':
            flash(result.message)
            return redirect(url_for('auth.login'))

        flash(result.message or '用户名或密码错误')
    elif form.errors:
        logger.debug('登录表单校验失败: %s', form.errors)

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.debug('已登录用户 %s 访问注册页，重定向至首页', current_user.username)
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        result = register_user(form.username.data, form.email.data, form.password.data)
        if result.success:
            flash('注册成功！请登录')
            return redirect(url_for('auth.login'))

        flash('注册失败: ' + (result.message or '请稍后重试'))

    if form.errors:
        logger.debug('注册表单校验错误: %s', form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}：{error}")

    return render_template('register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logger.info('用户 %s 退出系统', current_user.username)
    logout_user()
    flash('您已退出系统')
    return redirect(url_for('auth.login'))
