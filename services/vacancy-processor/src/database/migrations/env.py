import asyncio
from typing import Literal

from alembic import context
from common.database.config import db_config

# FIXME from core import service_config
from core.config import service_config
from database.models import Base
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.sql.schema import SchemaItem


config = context.config
config.set_main_option("sqlalchemy.url", db_config.url.render_as_string(hide_password=False))

# Models imports
# importlib.import_module("database.models.example_model")  # noqa: ERA001
target_metadata = Base.metadata


def include_object(
    obj: SchemaItem,
    _name: str | None,
    type_: Literal["schema", "table", "column", "index", "unique_constraint", "foreign_key_constraint"],
    _reflected: bool,  # noqa: FBT001
    _compare_to: SchemaItem | None,
) -> bool:
    return not (type_ == "table" and getattr(obj, "schema", None) != service_config.db_schema)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=service_config.db_schema,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=service_config.db_schema,
        include_object=include_object,
    )

    with context.begin_transaction():
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {service_config.db_schema}"))
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
