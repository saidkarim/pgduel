import pytest
from unittest.mock import patch, MagicMock
from lib.runner import Runner


# Mock DatabaseConnection and execute_query
@pytest.fixture
def mock_db_connection():
    with patch('lib.runner.DatabaseConnection') as MockDatabaseConnection:
        mock_instance = MockDatabaseConnection.return_value
        mock_instance.execute_query.return_value = MagicMock()
        yield mock_instance


def test_runner_initialization():
    dsn1 = "dbname=test1 user=user1 password=pass1 host=localhost port=5432"
    dsn2 = "dbname=test2 user=user2 password=pass2 host=localhost port=5433"
    query = "SELECT * FROM table"
    need_result = True

    runner = Runner(dsn1, dsn2, query, need_result)

    assert runner.dsn1 == dsn1
    assert runner.dsn2 == dsn2
    assert runner.query == query
    assert runner.need_result == need_result
    assert runner.results is None


def test_runner_start_method(mock_db_connection):
    dsn = "dbname=test user=user password=pass host=localhost port=5432"
    query = "SELECT * FROM table"
    need_result = True

    runner = Runner(dsn, dsn, query, need_result)
    result = runner._start(dsn)

    mock_db_connection.execute_query.assert_called_once_with(query=query, need_result=need_result)
    assert result == mock_db_connection.execute_query.return_value


def test_runner_start_all(mock_db_connection):
    dsn1 = "dbname=test1 user=user1 password=pass1 host=localhost port=5432"
    dsn2 = "dbname=test2 user=user2 password=pass2 host=localhost port=5433"
    query = "SELECT * FROM table"
    need_result = True

    runner = Runner(dsn1, dsn2, query, need_result)
    runner.start_all()

    assert len(runner.results) == 2
    assert mock_db_connection.execute_query.call_count == 2

