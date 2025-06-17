import logging
import time
from typing import Any
import warnings

from sqlalchemy import ClauseElement, Compiled, Connection, event
from sqlalchemy.dialects.postgresql.asyncpg import PGExecutionContext_asyncpg
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SAWarning
import sqlparse  # type: ignore[import-untyped]

from libs.logger import get_logger


__all__ = ["setup_alchemy_logging"]


logger = get_logger(__name__)

# Модуль подставляет значения в SQL запрос для логирования, поэтому корректность SQL запроса не так важна
# Например, возникает предупреждение о необходимости использовать "is NULL", а не "= NULL"
warnings.filterwarnings("ignore", category=SAWarning, module=__name__)


logging.getLogger("sqlalchemy.log").handlers.clear()


def setup_alchemy_logging() -> None:
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn: Connection, *_: Any) -> None:
        conn.info.setdefault("query_start_time", []).append(time.time())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(
            conn: Connection,
            _cursor: Any,
            statement: str,
            _parameters: Any,
            context: PGExecutionContext_asyncpg,
            _executemany: Any,
    ) -> None:
        total = time.time() - conn.info["query_start_time"].pop(-1)

        compiled = context.compiled
        if isinstance(compiled, Compiled) and isinstance(compiled.statement, ClauseElement):
            compiled_sql = compiled.statement.compile(dialect=compiled.dialect, compile_kwargs={"literal_binds": True})
            formatted_sql = sqlparse.format(str(compiled_sql), reindent=True, keyword_case="upper")
        else:
            formatted_sql = sqlparse.format(statement, reindent=True, keyword_case="upper")

        logger.debug("Query Time: %.5fs\n%s", total, formatted_sql)