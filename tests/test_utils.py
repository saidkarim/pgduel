from lib.utils import compose_dsn, Color


def test_compose_dsn_all_parameters():
    dsn = compose_dsn(
        host="localhost",
        port="5432",
        db_name="test_db",
        db_user="test_user",
        db_password="test_password"
    )
    expected_dsn = "postgresql://test_user:test_password@localhost:5432/test_db"
    assert dsn == expected_dsn


def test_compose_dsn_with_dsn():
    dsn_input = "postgresql://user:pass@host:port/dbname"
    dsn = compose_dsn(dsn=dsn_input)
    assert dsn == dsn_input


def test_compose_dsn_missing_parameters():
    dsn = compose_dsn(
        host="localhost",
        port="5432",
        db_name="test_db",
        db_user="test_user"
    )
    expected_dsn = "postgresql://test_user@localhost:5432/test_db"
    assert dsn == expected_dsn


def test_color_constants():
    assert Color.RESET == "\033[0m"
    assert Color.GREEN == "\033[92m"
