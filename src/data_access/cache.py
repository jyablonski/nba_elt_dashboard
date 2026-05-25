import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock

import pandas as pd
from sqlalchemy.engine.base import Engine

from src.data_access.database import get_dashboard_engine, get_data
from src.data_access.tables import source_tables

HIGH_LIMIT_TABLES = {"reddit_sentiment_time_series", "mov"}
HIGH_LIMIT_AMOUNT = 10_000_000
DEFAULT_LIMIT_AMOUNT = 2_000

_data_lock = RLock()
_data_snapshot: dict[str, pd.DataFrame] = {}
_snapshot_metadata: dict[str, object] = {
    "last_refreshed_at": None,
    "duration_seconds": None,
    "row_counts": {},
}


@dataclass(frozen=True)
class RefreshResult:
    refreshed_at: datetime
    duration_seconds: float
    row_counts: dict[str, int] = field(default_factory=dict)


def _table_key(table: str) -> str:
    return table.split(".")[-1]


def _limit_for_table(table: str) -> int:
    if _table_key(table) in HIGH_LIMIT_TABLES:
        return HIGH_LIMIT_AMOUNT
    return DEFAULT_LIMIT_AMOUNT


def _load_tables(postgres_engine: Engine, tables: list[str]) -> dict[str, pd.DataFrame]:
    fresh: dict[str, pd.DataFrame] = {}
    with postgres_engine.begin() as connection:
        for table in tables:
            fresh[_table_key(table)] = get_data(
                table_name=table,
                conn=connection,
                limit_amount=_limit_for_table(table),
            )
    return fresh


def _publish_snapshot(fresh: dict[str, pd.DataFrame], result: RefreshResult) -> None:
    global _data_snapshot

    with _data_lock:
        _data_snapshot = fresh
        _snapshot_metadata.update(
            {
                "last_refreshed_at": result.refreshed_at,
                "duration_seconds": result.duration_seconds,
                "row_counts": result.row_counts,
            }
        )


def generate_data(postgres_engine: Engine, source_tables: list[str]) -> None:
    refresh_data(postgres_engine=postgres_engine, tables=source_tables)


def refresh_data(
    postgres_engine: Engine | None = None,
    tables: list[str] | None = None,
) -> RefreshResult:
    active_engine = postgres_engine if postgres_engine is not None else get_dashboard_engine()
    active_tables = tables if tables is not None else source_tables
    started = time.monotonic()
    fresh = _load_tables(postgres_engine=active_engine, tables=active_tables)
    result = RefreshResult(
        refreshed_at=datetime.now(timezone.utc),
        duration_seconds=round(time.monotonic() - started, 3),
        row_counts={table: len(df) for table, df in fresh.items()},
    )
    _publish_snapshot(fresh=fresh, result=result)
    return result


def get_table(table_name: str) -> pd.DataFrame:
    with _data_lock:
        if table_name in _data_snapshot:
            return _data_snapshot[table_name].copy()

        raise KeyError(table_name)


def get_snapshot_metadata() -> dict[str, object]:
    with _data_lock:
        metadata = _snapshot_metadata.copy()
        metadata["row_counts"] = dict(_snapshot_metadata["row_counts"])
        return metadata


def has_snapshot() -> bool:
    with _data_lock:
        return bool(_data_snapshot)
