from logging.config import fileConfig

from pydantic_settings import BaseSettings, SettingsConfigDict

from alembic import context

import re

from sqlalchemy import create_engine


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Settings from env files
class MigrationSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    pg_host: str
    pg_port: str
    db_driver: str
    postgres_user: str
    postgres_password: str
    postgres_db: str


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    env_path = _get_env_path()
    settings = MigrationSettings(_env_file=env_path)
    url = _get_sqlalchemy_url_by_settings(settings)

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def _get_env_path() -> str:
    x_arguments = context.get_x_argument(as_dictionary=True)
    env_path = x_arguments.get("env_path")

    return env_path


def _get_sqlalchemy_url_by_settings(settings: MigrationSettings) -> str:
    url_tokens = {
        "DB_DRIVER": settings.db_driver,
        "DB_HOST": settings.pg_host,
        "DB_PORT": settings.pg_port,
        "DB_USER": settings.postgres_user,
        "DB_PASSWORD": settings.postgres_password,
        "DB_NAME": settings.postgres_db,
    }

    url = config.get_main_option("sqlalchemy.url")
    url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)

    return url


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
