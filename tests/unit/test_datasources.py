"""Tests for data source implementations."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from report_generator.datasources.api import APISource
from report_generator.datasources.database import DatabaseSource
from report_generator.datasources.file import FileSource
from report_generator.utils.exceptions import DataSourceError, ValidationError


class TestFileSource:
    """Tests for FileSource class."""

    def test_csv_file_read(self, tmp_path: Path) -> None:
        """Test reading a CSV file."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,value\nAlice,100\nBob,200\n")

        source = FileSource(name="test_csv", file_path=str(csv_file))
        df = source.fetch()

        assert len(df) == 2
        assert list(df.columns) == ["name", "value"]
        assert df.iloc[0]["name"] == "Alice"

    def test_csv_with_custom_delimiter(self, tmp_path: Path) -> None:
        """Test reading CSV with custom delimiter."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name;value\nAlice;100\nBob;200\n")

        source = FileSource(
            name="test_csv",
            file_path=str(csv_file),
            config={"delimiter": ";"},
        )
        df = source.fetch()

        assert len(df) == 2
        assert df.iloc[0]["value"] == 100

    def test_json_file_read(self, tmp_path: Path) -> None:
        """Test reading a JSON file."""
        json_file = tmp_path / "data.json"
        data = [{"name": "Alice", "value": 100}, {"name": "Bob", "value": 200}]
        json_file.write_text(json.dumps(data))

        source = FileSource(name="test_json", file_path=str(json_file))
        df = source.fetch()

        assert len(df) == 2
        assert list(df.columns) == ["name", "value"]

    def test_excel_file_read(self, tmp_path: Path) -> None:
        """Test reading an Excel file."""
        excel_file = tmp_path / "data.xlsx"
        df_write = pd.DataFrame({"name": ["Alice", "Bob"], "value": [100, 200]})
        df_write.to_excel(excel_file, index=False)

        source = FileSource(name="test_excel", file_path=str(excel_file))
        df = source.fetch()

        assert len(df) == 2
        assert list(df.columns) == ["name", "value"]

    def test_file_not_found(self) -> None:
        """Test error when file doesn't exist."""
        with pytest.raises(DataSourceError) as exc_info:
            FileSource(name="missing", file_path="/nonexistent/file.csv")

        assert "File not found" in str(exc_info.value)

    def test_unsupported_format(self, tmp_path: Path) -> None:
        """Test error for unsupported file format."""
        txt_file = tmp_path / "data.txt"
        txt_file.write_text("some text")

        source = FileSource(name="test_txt", file_path=str(txt_file))

        with pytest.raises(DataSourceError) as exc_info:
            source.fetch()

        assert "Unsupported file format" in str(exc_info.value)

    def test_test_connection_csv(self, tmp_path: Path) -> None:
        """Test connection test for CSV file."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,value\nAlice,100\n")

        source = FileSource(name="test_csv", file_path=str(csv_file))
        assert source.test_connection() is True

    def test_test_connection_json(self, tmp_path: Path) -> None:
        """Test connection test for JSON file."""
        json_file = tmp_path / "data.json"
        json_file.write_text('[{"name": "Alice"}]')

        source = FileSource(name="test_json", file_path=str(json_file))
        assert source.test_connection() is True

    def test_test_connection_excel(self, tmp_path: Path) -> None:
        """Test connection test for Excel file."""
        excel_file = tmp_path / "data.xlsx"
        df = pd.DataFrame({"name": ["Alice"]})
        df.to_excel(excel_file, index=False)

        source = FileSource(name="test_excel", file_path=str(excel_file))
        assert source.test_connection() is True


class TestAPISource:
    """Tests for APISource class."""

    def test_init_with_auth_token(self) -> None:
        """Test initialization with auth token."""
        source = APISource(
            name="test_api",
            url="https://api.example.com/data",
            auth_token="secret-token",
        )

        assert source.headers["Authorization"] == "Bearer secret-token"

    def test_init_with_custom_headers(self) -> None:
        """Test initialization with custom headers."""
        source = APISource(
            name="test_api",
            url="https://api.example.com/data",
            headers={"X-Custom": "value"},
        )

        assert source.headers["X-Custom"] == "value"

    def test_invalid_url(self) -> None:
        """Test error for invalid URL."""
        with pytest.raises(ValidationError):
            APISource(name="test_api", url="not-a-valid-url")

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_get_list_response(self, mock_session_class: MagicMock) -> None:
        """Test fetch with GET request returning list."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response

        source = APISource(name="test_api", url="https://api.example.com/items")
        df = source.fetch()

        assert len(df) == 2
        assert list(df.columns) == ["id", "name"]

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_get_dict_with_data_key(self, mock_session_class: MagicMock) -> None:
        """Test fetch with response containing 'data' key."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{"id": 1}, {"id": 2}],
            "meta": {"total": 2},
        }
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response

        source = APISource(name="test_api", url="https://api.example.com/items")
        df = source.fetch()

        assert len(df) == 2

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_get_dict_with_results_key(self, mock_session_class: MagicMock) -> None:
        """Test fetch with response containing 'results' key."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [{"id": 1}, {"id": 2}],
            "count": 2,
        }
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response

        source = APISource(name="test_api", url="https://api.example.com/items")
        df = source.fetch()

        assert len(df) == 2

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_get_single_dict(self, mock_session_class: MagicMock) -> None:
        """Test fetch with single dict response (no data/results key)."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Single Item"}
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response

        source = APISource(name="test_api", url="https://api.example.com/item/1")
        df = source.fetch()

        assert len(df) == 1
        assert df.iloc[0]["name"] == "Single Item"

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_post_request(self, mock_session_class: MagicMock) -> None:
        """Test fetch with POST request."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1}]
        mock_response.status_code = 200
        mock_session.post.return_value = mock_response

        source = APISource(
            name="test_api",
            url="https://api.example.com/query",
            method="POST",
            data={"filter": "active"},
        )
        df = source.fetch()

        assert len(df) == 1
        mock_session.post.assert_called_once()

    @patch("report_generator.datasources.api.requests.Session")
    def test_fetch_unsupported_method(self, mock_session_class: MagicMock) -> None:
        """Test error for unsupported HTTP method."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        source = APISource(
            name="test_api",
            url="https://api.example.com/data",
            method="DELETE",
        )

        with pytest.raises(DataSourceError) as exc_info:
            source.fetch()

        assert "Unsupported HTTP method" in str(exc_info.value)

    @patch("report_generator.datasources.api.requests.Session")
    def test_test_connection_success(self, mock_session_class: MagicMock) -> None:
        """Test successful connection test."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.head.return_value = mock_response

        source = APISource(name="test_api", url="https://api.example.com/health")
        assert source.test_connection() is True


class TestDatabaseSource:
    """Tests for DatabaseSource class."""

    def test_sqlite_fetch(self, tmp_path: Path) -> None:
        """Test fetching data from SQLite database."""
        db_path = tmp_path / "test.db"

        # Create test database with data
        import sqlite3

        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        conn.execute("INSERT INTO users VALUES (2, 'Bob')")
        conn.commit()
        conn.close()

        source = DatabaseSource(
            name="test_db",
            connection_string=f"sqlite:///{db_path}",
            query="SELECT * FROM users",
        )
        df = source.fetch()

        assert len(df) == 2
        assert list(df.columns) == ["id", "name"]
        assert df.iloc[0]["name"] == "Alice"

        source.close()

    def test_sqlite_test_connection(self, tmp_path: Path) -> None:
        """Test connection test for SQLite."""
        db_path = tmp_path / "test.db"

        # Create empty database
        import sqlite3

        conn = sqlite3.connect(str(db_path))
        conn.close()

        source = DatabaseSource(
            name="test_db",
            connection_string=f"sqlite:///{db_path}",
            query="SELECT 1",
        )

        assert source.test_connection() is True
        source.close()

    def test_close_engine(self, tmp_path: Path) -> None:
        """Test closing database engine."""
        db_path = tmp_path / "test.db"

        import sqlite3

        conn = sqlite3.connect(str(db_path))
        conn.close()

        source = DatabaseSource(
            name="test_db",
            connection_string=f"sqlite:///{db_path}",
            query="SELECT 1",
        )

        # Access engine to initialize it
        _ = source.engine
        assert source._engine is not None

        source.close()
        assert source._engine is None

    def test_engine_lazy_initialization(self, tmp_path: Path) -> None:
        """Test that engine is lazily initialized."""
        db_path = tmp_path / "test.db"

        import sqlite3

        conn = sqlite3.connect(str(db_path))
        conn.close()

        source = DatabaseSource(
            name="test_db",
            connection_string=f"sqlite:///{db_path}",
            query="SELECT 1",
        )

        # Engine should not be created yet
        assert source._engine is None

        # Access engine property
        engine = source.engine
        assert engine is not None
        assert source._engine is not None

        source.close()
