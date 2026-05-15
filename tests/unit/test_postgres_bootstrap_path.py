from tests.postgres_bootstrap import bootstrap_sql_path


def test_bootstrap_sql_file_exists():
    assert bootstrap_sql_path().is_file()
