import os
from datetime import timedelta


def strtobool(value, default=False):
    """将环境变量解析为布尔值"""
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'  # TODO: 生产环境中使用环境变量

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 安全配置
    WTF_CSRF_ENABLED = True

    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_ROTATION = os.environ.get('LOG_ROTATION', '20 MB')
    LOG_RETENTION = os.environ.get('LOG_RETENTION', '14 days')
    LOG_BACKTRACE = strtobool(os.environ.get('LOG_BACKTRACE'), False)
    LOG_DIAGNOSE = strtobool(os.environ.get('LOG_DIAGNOSE'), False)
    LOG_PATH = os.environ.get('LOG_PATH')
    LOG_DIR = os.environ.get('LOG_DIR')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # TODO: 添加生产环境特定配置


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
