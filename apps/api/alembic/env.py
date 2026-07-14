import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Import every context's SQLAlchemy models here so Base.metadata knows about
# them for autogenerate. One line per context as infrastructure models land —
# this file is the one place that needs to know all contexts exist.
from northstar.contexts.companies.infrastructure import (
    models as companies_models,  # noqa: E402,F401
)
from northstar.contexts.geo.infrastructure import (
    models as geo_models,  # noqa: E402,F401
)
from northstar.platform.config import get_settings  # noqa: E402
from northstar.platform.db import Base  # noqa: E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Config is env-only (ADR 0003) — the DB URL comes from Settings, never a
# hardcoded value in alembic.ini.
target_metadata = Base.metadata

# PostGIS/pgvector install their own system tables (spatial_ref_sys, the
# topology schema, …) directly into the database, outside our SQLAlchemy
# metadata. Without this filter, autogenerate proposes dropping them on every
# revision — exclude anything our models don't own.
_POSTGIS_SYSTEM_TABLES = {"spatial_ref_sys"}


def include_object(
    object: object, name: str, type_: str, reflected: bool, compare_to: object
) -> bool:
    return not (type_ == "table" and name in _POSTGIS_SYSTEM_TABLES)


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
