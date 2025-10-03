from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from loguru import logger

# 初始化扩展

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
cors = CORS()

from config import config
from app.utils.logging import configure_logging
from app.utils.bootstrap import ensure_seed_data


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    configure_logging(app)

    # 配置 CORS
    app.config['CORS_HEADERS'] = 'Content-Type'

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # 设置登录视图
    login_manager.login_view = 'auth.login'
    login_manager.login_message = None  # 禁用自动登录消息

    # 注册蓝图
    from .controllers.auth import auth_bp
    from .controllers.user import user_bp
    from .controllers.group import group_bp
    from .controllers.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(group_bp, url_prefix='/groups')
    app.register_blueprint(main_bp)

    # 注册错误处理
    register_error_handlers(app)

    # 注册命令
    from .commands import init_db_command
    app.cli.add_command(init_db_command)

    with app.app_context():
        db.create_all()
        ensure_seed_data()

    logger.info('应用已启动，配置: {}', config_name)

    return app


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        logger.warning('未找到页面: {}', e)
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.exception('服务器内部错误')
        return render_template('errors/500.html'), 500
