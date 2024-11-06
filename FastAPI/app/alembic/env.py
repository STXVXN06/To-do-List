"""
Este módulo configura Alembic para manejar migraciones de base de datos.

Se encarga de establecer la conexión a la base de datos y definir
el comportamiento de las migraciones, tanto en modo 'offline' como 'online'.
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from migrations import Base, DATABASE_URL  # pylint: disable=import-error

# Este objeto de configuración de Alembic proporciona acceso a los
# valores dentro del archivo .ini en uso.
config = context.config  # pylint: disable=no-member
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpreta el archivo de configuración para la configuración de registro.
# Esta línea configura los registradores en esencia.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agrega el objeto MetaData de tu modelo aquí para el soporte de 'autogenerar'
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'.

    Esto configura el contexto solo con una URL y no con un Engine,
    aunque un Engine es aceptable aquí también. Al omitir la creación
    del Engine, ni siquiera necesitamos que un DBAPI esté disponible.

    Las llamadas a context.execute() aquí emiten la cadena dada en
    la salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure( # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction(): # pylint: disable=no-member
        context.run_migrations() # pylint: disable=no-member

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'.

    En este escenario, necesitamos crear un Engine y asociar una
    conexión con el contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata) # pylint: disable=no-member

        with context.begin_transaction(): # pylint: disable=no-member
            context.run_migrations() # pylint: disable=no-member

if context.is_offline_mode(): # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()