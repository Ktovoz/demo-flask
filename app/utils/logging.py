import logging
import sys
from pathlib import Path

from loguru import logger


class InterceptHandler(logging.Handler):
    """将标准库 logging 输出转发到 Loguru"""

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        logger.opt(exception=record.exc_info, depth=6).log(level, record.getMessage())


def configure_logging(app):
    """配置 Loguru 日志输出"""
    if app.config.get('LOGURU_CONFIGURED'):
        return

    logger.remove()

    log_level = app.config.get('LOG_LEVEL', 'INFO')
    backtrace = app.config.get('LOG_BACKTRACE', False)
    diagnose = app.config.get('LOG_DIAGNOSE', False)

    logger.add(sys.stdout, level=log_level, enqueue=True, backtrace=backtrace, diagnose=diagnose)

    log_path_value = app.config.get('LOG_PATH')
    if log_path_value:
        log_path = Path(log_path_value)
    else:
        log_dir_value = app.config.get('LOG_DIR')
        log_dir = Path(log_dir_value) if log_dir_value else (Path(app.instance_path) / 'logs')
        log_path = log_dir / 'app.log'

    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path,
        level=log_level,
        rotation=app.config.get('LOG_ROTATION', '20 MB'),
        retention=app.config.get('LOG_RETENTION', '14 days'),
        enqueue=True,
        backtrace=backtrace,
        diagnose=diagnose,
        encoding='utf-8'
    )

    intercept_handler = InterceptHandler()
    logging.root.handlers = [intercept_handler]
    logging.root.setLevel(logging.NOTSET)

    if isinstance(log_level, str):
        numeric_level = logging._nameToLevel.get(log_level.upper(), logging.INFO)
    else:
        numeric_level = log_level

    app.logger.handlers = [intercept_handler]
    app.logger.setLevel(numeric_level)
    app.logger.propagate = False

    for name in ('werkzeug', 'gunicorn.error', 'gunicorn.access'):
        logger_instance = logging.getLogger(name)
        logger_instance.handlers = [intercept_handler]
        logger_instance.setLevel(numeric_level)
        logger_instance.propagate = False

    app.config['LOGURU_CONFIGURED'] = True
    app.logger.info('Loguru 日志已配置，输出文件: %s', log_path)
