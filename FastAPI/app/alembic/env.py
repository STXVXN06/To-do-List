# pylint: disable=import-error, no-member
"""
This module configures Alembic to handle database migrations.

It is responsible for establishing the connection to the database and defining the behavior of the
the behavior of migrations, both in 'offline' and 'online' mode.
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from migrations import Base, DATABASE_URL
from alembic import context

# Alembic configuration for accessing values in the .ini file
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configuration of logging from the configuration file, if any
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model MetaData for autogeneration support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Execute migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Execute migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determines the execution mode and calls the corresponding function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
