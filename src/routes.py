import os
from pathlib import Path

from flask import Flask, jsonify, request

from src.data_access.cache import get_snapshot_metadata, has_snapshot
from src.data_access.cache import refresh_data as refresh_dashboard_data

PROC_STATM_PATH = Path("/proc/self/statm")
CGROUP_V2_MEMORY_CURRENT_PATH = Path("/sys/fs/cgroup/memory.current")
CGROUP_V2_MEMORY_MAX_PATH = Path("/sys/fs/cgroup/memory.max")
CGROUP_V1_MEMORY_CURRENT_PATH = Path("/sys/fs/cgroup/memory/memory.usage_in_bytes")
CGROUP_V1_MEMORY_LIMIT_PATH = Path("/sys/fs/cgroup/memory/memory.limit_in_bytes")


def _bytes_to_mb(value: int | None) -> float | None:
    if value is None:
        return None
    return round(value / 1024 / 1024, 1)


def _read_int_file(path: Path) -> int | None:
    try:
        value = path.read_text().strip()
    except OSError:
        return None
    if not value or value == "max":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _process_rss_bytes() -> int | None:
    try:
        statm = PROC_STATM_PATH.read_text().split()
        resident_pages = int(statm[1])
        page_size = os.sysconf("SC_PAGE_SIZE")
    except OSError, IndexError, ValueError:
        return None
    return resident_pages * page_size


def _container_memory_bytes() -> tuple[int | None, int | None]:
    current = _read_int_file(CGROUP_V2_MEMORY_CURRENT_PATH)
    limit = _read_int_file(CGROUP_V2_MEMORY_MAX_PATH)
    if current is not None or limit is not None:
        return current, limit

    return (
        _read_int_file(CGROUP_V1_MEMORY_CURRENT_PATH),
        _read_int_file(CGROUP_V1_MEMORY_LIMIT_PATH),
    )


def _memory_metadata() -> dict[str, float | None]:
    container_current, container_limit = _container_memory_bytes()
    return {
        "process_rss_mb": _bytes_to_mb(_process_rss_bytes()),
        "container_current_mb": _bytes_to_mb(container_current),
        "container_limit_mb": _bytes_to_mb(container_limit),
    }


def _validate_internal_token():
    expected_token = os.environ.get("DATA_REFRESH_TOKEN")
    provided_token = request.headers.get("X-Refresh-Token")

    if not expected_token:
        return jsonify({"error": "DATA_REFRESH_TOKEN is not configured"}), 500

    if provided_token != expected_token:
        return jsonify({"error": "unauthorized"}), 401

    return None


def register_routes(server: Flask) -> None:
    """Attach the internal ops endpoints and data-load hook to the Flask server."""

    @server.post("/internal/refresh-data")
    def refresh_data_endpoint():
        token_error = _validate_internal_token()
        if token_error is not None:
            return token_error

        result = refresh_dashboard_data()
        return jsonify(
            {
                "status": "ok",
                "refreshed_at": result.refreshed_at.isoformat(),
                "duration_seconds": result.duration_seconds,
                "row_counts": result.row_counts,
            }
        )

    @server.get("/internal/health")
    def health_endpoint():
        token_error = _validate_internal_token()
        if token_error is not None:
            return token_error

        metadata = get_snapshot_metadata()
        snapshot_ready = has_snapshot()
        last_refreshed_at = metadata["last_refreshed_at"]
        return (
            jsonify(
                {
                    "status": "ok" if snapshot_ready else "unavailable",
                    "has_snapshot": snapshot_ready,
                    "last_refreshed_at": (
                        last_refreshed_at.isoformat() if last_refreshed_at is not None else None
                    ),
                    "duration_seconds": metadata["duration_seconds"],
                    "row_counts": metadata["row_counts"],
                    "memory": _memory_metadata(),
                }
            ),
            200 if snapshot_ready else 503,
        )

    @server.before_request
    def ensure_dashboard_data_loaded():
        if request.path.startswith("/internal/"):
            return None
        if not has_snapshot():
            refresh_dashboard_data()
        return None
