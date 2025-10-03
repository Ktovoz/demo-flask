import click
from flask.cli import with_appcontext
from loguru import logger

from app import db
from app.utils.bootstrap import ensure_seed_data


@click.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库并准备演示账号"""
    logger.info('开始执行 init-db 命令')
    db.create_all()

    created_groups, created_users = ensure_seed_data(commit=True)
    if not created_groups and not created_users:
        logger.debug('默认数据已存在，无需变更')

    logger.success('init-db 执行完成')
    click.echo('数据库初始化完成，默认账号已准备就绪。')
