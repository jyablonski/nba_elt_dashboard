import inspect

import pytest

from src.mcp_server import gold_queries
from src.mcp_server.gold_queries import QUERY_DIR, load_query


def _query_names() -> set[str]:
    return {path.stem for path in QUERY_DIR.glob("*.sql")}


def test_every_sql_file_is_loaded_by_a_function():
    """No orphaned .sql files — a query nobody calls is a query nobody maintains."""
    source = inspect.getsource(gold_queries)
    unreferenced = {name for name in _query_names() if f'load_query("{name}")' not in source}

    assert unreferenced == set()


def test_every_loaded_query_has_a_file():
    for name in _query_names():
        assert load_query(name).strip()


def test_load_query_rejects_path_traversal():
    with pytest.raises(ValueError, match="invalid query name"):
        load_query("../../../etc/passwd")


def test_queries_are_parameterized_not_formatted():
    """Guard against reintroducing string-built SQL: no % or {} placeholders."""
    for name in _query_names():
        sql = load_query(name)
        assert "%s" not in sql, f"{name}.sql uses %s formatting"
        assert "{" not in sql, f"{name}.sql looks f-string formatted"


def test_query_files_follow_the_house_style():
    """4-space indent, and select/group by/order by items on their own lines."""
    for name in _query_names():
        lines = load_query(name).splitlines()
        for number, line in enumerate(lines, start=1):
            if not line.strip() or line.startswith("--"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            assert indent % 4 == 0, f"{name}.sql:{number} indent {indent} is not a multiple of 4"
            assert "\t" not in line, f"{name}.sql:{number} uses a tab"

        # A clause keyword never shares a line with its items. Subselects are indented
        # and start with "(", so they don't trip this.
        for clause in ("select", "group by", "order by"):
            offenders = [line for line in lines if line.strip().lower().startswith(f"{clause} ")]
            assert not offenders, (
                f"{name}.sql puts items on the same line as `{clause}`: {offenders}"
            )
