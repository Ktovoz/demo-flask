from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger

from app.forms.auth import LoginForm, RegistrationForm
from app.services.auth_service import authenticate_user, register_user
from app.utils.request_logger import log_user_action


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录路由
    
    GET请求: 显示登录表单页面
    POST请求: 处理登录表单提交
    """
    if current_user.is_authenticated:
        logger.debug('已登录用户 %s 访问登录页，重定向至首页', current_user.username)
        log_user_action("访问登录页（已登录）", user=current_user)
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        result = authenticate_user(form.username.data, form.password.data)
        if result.success and result.user:
            login_user(result.user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            # 记录登录成功行为
            log_user_action(
                "登录成功",
                user=result.user,
                extra_data={
                    "记住我": form.remember_me.data,
                    "重定向页面": next_page
                }
            )
            
            return redirect(next_page)

        if result.status == 'disabled':
            flash(result.message)
            # 记录登录失败行为
            log_user_action(
                "登录失败",
                extra_data={
                    "用户名": form.username.data,
                    "原因": "账户被禁用"
                }
            )
            return redirect(url_for('auth.login'))

        flash(result.message or '用户名或密码错误')
        # 记录登录失败行为
        log_user_action(
            "登录失败",
            extra_data={
                "用户名": form.username.data,
                "原因": "用户名或密码错误"
            }
        )
    elif form.errors:
        logger.debug('登录表单校验失败: %s', form.errors)
        log_user_action(
            "登录表单校验失败",
            extra_data={
                "错误信息": form.errors
            }
        )

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册路由
    
    GET请求: 显示注册表单页面
    POST请求: 处理注册表单提交
    """
    if current_user.is_authenticated:
        logger.debug('已登录用户 %s 访问注册页，重定向至首页', current_user.username)
        log_user_action("访问注册页（已登录）", user=current_user)
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        result = register_user(form.username.data, form.email.data, form.password.data)
        if result.success:
            flash('注册成功！请登录')
            # 记录注册成功行为
            log_user_action(
                "注册成功",
                extra_data={
                    "用户名": form.username.data,
                    "邮箱": form.email.data
                }
            )
            return redirect(url_for('auth.login'))

        flash('注册失败: ' + (result.message or '请稍后重试'))
        # 记录注册失败行为
        log_user_action(
            "注册失败",
            extra_data={
                "用户名": form.username.data,
                "邮箱": form.email.data,
                "原因": result.message or '未知错误'
            }
        )

    if form.errors:
        logger.debug('注册表单校验错误: %s', form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}：{error}")
        # 记录表单校验错误
        log_user_action(
            "注册表单校验失败",
            extra_data={
                "错误信息": form.errors
            }
        )

    return render_template('register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """用户退出登录路由
    
    仅允许已登录用户访问，处理用户退出登录逻辑
    """
    logger.info('用户 %s 退出系统', current_user.username)
    # 记录退出系统行为
    log_user_action("退出系统", user=current_user)
    logout_user()
    flash('您已退出系统')
    return redirect(url_for('auth.login'))
