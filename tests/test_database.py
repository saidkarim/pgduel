import pytest
from unittest.mock import patch, Mock
import psycopg2
from lib.database import DatabaseConnection, DatabaseConnectionExecutionError, QueryMetric
from contextlib import nullcontext


@pytest.fixture
def db_connection():
    return DatabaseConnection(
        host="localhost",
        port=5432,
        db_name="test_db",
        db_user="test_user",
        db_password="test_password"
    )


@pytest.fixture
def mock_connect():
    with patch("lib.database.psycopg2.connect") as mock_connect:
        yield mock_connect


def test_database_connection_initialization(db_connection):
    assert db_connection.host == "localhost"
    assert db_connection.port == 5432
    assert db_connection.db_name == "test_db"
    assert db_connection.db_user == "test_user"
    assert db_connection.db_password == "test_password"
    assert db_connection.dsn is not None


def test_dsn_composition(db_connection):
    expected_dsn = "postgresql://test_user:test_password@localhost:5432/test_db"
    assert db_connection.dsn == expected_dsn


def test_execute_query_success(db_connection, mock_connect):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = nullcontext(mock_cursor)

    mock_cursor.fetchall.return_value = [("result1",), ("result2",)]

    query = "SELECT * FROM table"
    result = db_connection.execute_query(query, need_result=True)

    assert isinstance(result, QueryMetric)
    assert result.result == [("result1",), ("result2",)]
    assert result.timing > 0


def test_execute_query_no_result(db_connection, mock_connect):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = nullcontext(mock_cursor)

    query = "SELECT * FROM table"
    result = db_connection.execute_query(query, need_result=False)

    assert isinstance(result, QueryMetric)
    assert result.result == []
    assert result.timing > 0


def test_execute_query_error(db_connection, mock_connect):
    mock_connect.side_effect = psycopg2.OperationalError

    query = "SELECT * FROM table"
    with pytest.raises(DatabaseConnectionExecutionError):
        db_connection.execute_query(query)
