from unittest.mock import patch, MagicMock
import pytest
from pytest_mock import mocker
from database import Database


@pytest.fixture
def mock_sqlite_connect(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    return mock_connect

@pytest.fixture
def mock_psycopg2_connect(mocker):
    mock_connect = mocker.patch('psycopg2.connect')
    return mock_connect

@pytest.fixture
def mock_mysql_connect(mocker):
    mock_connect = mocker.patch('mysql.connector.connect')
    return mock_connect

def test_sqlite_connection(mock_sqlite_connect):
    db = Database('sqlite:///test.db')
    mock_sqlite_connect.assert_called_once_with('test.db')

def test_postgresql_connection(mock_psycopg2_connect):
    db = Database('postgresql://user:password@localhost:5432/testdb')
    mock_psycopg2_connect.assert_called_once_with(
        dbname='testdb',
        user='user',
        password='password',
        host='localhost',
        port=5432
    )

def test_mysql_connection(mock_mysql_connect):
    db = Database('mysql://user:password@localhost:3306/testdb')
    mock_mysql_connect.assert_called_once_with(
        database='testdb',
        user='user',
        password='password',
        host='localhost',
        port=3306
    )

def test_execute(mock_sqlite_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_sqlite_connect.return_value = mock_conn

    db = Database('sqlite:///test.db')
    db.execute('SELECT 1')

    mock_cursor.execute.assert_called_once_with('SELECT 1', ())
    mock_conn.commit.assert_called_once()

    db.execute('SELECT 1 WHERE id=?', (1,))
    mock_cursor.execute.assert_called_with('SELECT 1 WHERE id=?', (1,))


# def test_db_raises_error(unsupported_url):
#     with pytest.raises(ValueError, match="Unsupported database scheme: unsupported"):
#         Database(unsupported_url)