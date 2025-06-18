import importlib
from pathlib import Path
import sys

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
import uvloop


config = context.config
service = config.config_ini_section

# add libs and services to path for fix import error
PROJECT_ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "services" / service / "src"))

# load .env for pydantic settings
load_dotenv(PROJECT_ROOT / ".env")

# service and libs imports. Prefer use project root imports
# isort: off
from libs.database.config import DatabaseConfig # need use NEW db_config for replace db_config.host
# isort: on

db_config = DatabaseConfig()
db_config.host = "localhost"

db_url = db_config.url.render_as_string(hide_password=False)
config.set_main_option("sqlalchemy.url", db_url)

target_metadata = importlib.import_module(f"database.models").Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
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
    uvloop.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
