from flask import Flask, render_template
from loguru import logger

from config import config
from app.extensions import csrf, cors, db, login_manager, migrate
from app.utils.bootstrap import ensure_seed_data
from app.utils.logging import configure_logging


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    configure_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_cli(app)

    with app.app_context():
        db.create_all()
        ensure_seed_data()

    logger.info('应用已启动，配置: {}', config_name)
    return app


def register_extensions(app: Flask) -> None:
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    login_manager.login_view = 'auth.login'
    login_manager.login_message = None


def register_blueprints(app: Flask) -> None:
    from .controllers.auth import auth_bp
    from .controllers.group import group_bp
    from .controllers.main import main_bp
    from .controllers.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(group_bp, url_prefix='/groups')
    app.register_blueprint(main_bp)


def register_cli(app: Flask) -> None:
    from .commands import init_db_command

    app.cli.add_command(init_db_command)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        logger.warning('未找到页面: {}', error)
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.exception('服务器内部错误')
        return render_template('errors/500.html'), 500
