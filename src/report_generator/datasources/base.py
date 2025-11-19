"""Base data source abstract class."""

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from report_generator.utils.logger import get_logger

logger = get_logger(__name__)


class DataSource(ABC):
    """
    Abstract base class for all data sources.

    All data sources (databases, APIs, files) must implement this interface.
    """

    def __init__(self, name: str, config: dict[str, Any] | None = None) -> None:
        """
        Initialize data source.

        Args:
            name: Human-readable name for this data source
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        logger.info("datasource_initialized", name=name, type=self.__class__.__name__)

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        """
        Fetch data from the source.

        Returns:
            DataFrame containing the fetched data

        Raises:
            DataSourceError: If data fetching fails
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if the data source is accessible.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @classmethod
    def from_database(
        cls, connection_string: str, query: str, name: str = "database"
    ) -> "DataSource":
        """
        Create a database data source.

        Args:
            connection_string: SQLAlchemy connection string
            query: SQL query to execute
            name: Name for this data source

        Returns:
            DatabaseSource instance

        Example:
            >>> source = DataSource.from_database(
            ...     "postgresql://user:pass@localhost/db",
            ...     "SELECT * FROM orders"
            ... )
        """
        from report_generator.datasources.database import DatabaseSource

        return DatabaseSource(name=name, connection_string=connection_string, query=query)

    @classmethod
    def from_api(
        cls,
        url: str,
        method: str = "GET",
        auth_token: str | None = None,
        name: str = "api",
    ) -> "DataSource":
        """
        Create an API data source.

        Args:
            url: API endpoint URL
            method: HTTP method (GET, POST)
            auth_token: Authentication token
            name: Name for this data source

        Returns:
            APISource instance

        Example:
            >>> source = DataSource.from_api(
            ...     "https://api.example.com/data",
            ...     auth_token="your-token"
            ... )
        """
        from report_generator.datasources.api import APISource

        return APISource(name=name, url=url, method=method, auth_token=auth_token)

    @classmethod
    def from_file(cls, file_path: str, name: str = "file") -> "DataSource":
        """
        Create a file data source.

        Args:
            file_path: Path to CSV, Excel, or JSON file
            name: Name for this data source

        Returns:
            FileSource instance

        Example:
            >>> source = DataSource.from_file("data/sales.csv")
        """
        from report_generator.datasources.file import FileSource

        return FileSource(name=name, file_path=file_path)

    def __repr__(self) -> str:
        """String representation of data source."""
        return f"{self.__class__.__name__}(name='{self.name}')"
