"""
This module configures Alembic to handle database migrations.

It is responsible for establishing the connection to the database and defining
the behavior of migrations, both in 'offline' and 'online' modes.
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from migrations import Base, DATABASE_URL  # pylint: disable=import-error

# This Alembic configuration object provides access to the
# values within the ini file in use.
config = context.config  # pylint: disable=no-member
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for logging configuration.
# This line essentially configures the loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not with an Engine,
    although an Engine is also acceptable here. By skipping the creation
    of the Engine, we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to
    the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(  # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine and associate a
    connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)  # pylint: disable=no-member

        with context.begin_transaction():  # pylint: disable=no-member
            context.run_migrations()  # pylint: disable=no-member

if context.is_offline_mode():  # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()
