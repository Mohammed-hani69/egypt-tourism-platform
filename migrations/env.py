from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context
from sqlalchemy import engine_from_config, pool

# إعدادات Alembic
config = context.config

# إعدادات اللوج
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# إعداد قاعدة البيانات من Flask
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace('%', '%%')
)

target_metadata = current_app.extensions['migrate'].db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        render_as_batch=True  # مهم لـ SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = current_app.extensions['migrate'].db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # SQLite فقط يحتاج هذا
            dialect_opts={"paramstyle": "named"}
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
