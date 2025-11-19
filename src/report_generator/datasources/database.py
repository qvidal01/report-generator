"""Database data source implementation."""

from typing import Any

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from report_generator.datasources.base import DataSource
from report_generator.utils.exceptions import DataSourceError
from report_generator.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseSource(DataSource):
    """
    Data source for SQL databases using SQLAlchemy.

    Supports PostgreSQL, MySQL, SQLite, and other SQLAlchemy-compatible databases.
    """

    def __init__(
        self,
        name: str,
        connection_string: str,
        query: str,
        config: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize database source.

        Args:
            name: Name for this data source
            connection_string: SQLAlchemy connection URL
                Examples:
                - postgresql://user:pass@localhost/db
                - mysql+pymysql://user:pass@localhost/db
                - sqlite:///path/to/database.db
            query: SQL query to execute
            config: Additional configuration (connection pooling, etc.)
        """
        super().__init__(name, config)
        self.connection_string = connection_string
        self.query = query
        self._engine: Engine | None = None

    @property
    def engine(self) -> Engine:
        """
        Get SQLAlchemy engine (lazy initialization).

        Returns:
            SQLAlchemy Engine instance
        """
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self.connection_string,
                    pool_pre_ping=True,  # Verify connections before using
                    echo=False,  # Set to True for SQL logging
                )
                logger.info(
                    "database_engine_created",
                    name=self.name,
                    dialect=self._engine.dialect.name,
                )
            except Exception as e:
                raise DataSourceError(
                    f"Failed to create database engine: {e}", source_type="database"
                )
        return self._engine

    def fetch(self) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame.

        Returns:
            DataFrame with query results

        Raises:
            DataSourceError: If query execution fails

        Example:
            >>> source = DatabaseSource(
            ...     name="sales",
            ...     connection_string="postgresql://user:pass@localhost/db",
            ...     query="SELECT * FROM orders WHERE date >= '2025-01-01'"
            ... )
            >>> df = source.fetch()
        """
        logger.info("fetching_data", source=self.name, query=self.query[:100])

        try:
            # Use pandas read_sql for easy DataFrame conversion
            # Use text() for parameterized queries (prevents SQL injection)
            df = pd.read_sql(text(self.query), self.engine)

            logger.info(
                "data_fetched",
                source=self.name,
                rows=len(df),
                columns=len(df.columns),
            )
            return df

        except Exception as e:
            logger.error(
                "fetch_failed",
                source=self.name,
                error=str(e),
            )
            raise DataSourceError(
                f"Failed to fetch data from database '{self.name}': {e}",
                source_type="database",
            )

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful

        Raises:
            DataSourceError: If connection fails
        """
        try:
            with self.engine.connect() as conn:
                # Simple query to test connection
                conn.execute(text("SELECT 1"))
            logger.info("connection_test_passed", source=self.name)
            return True
        except Exception as e:
            logger.error("connection_test_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"Database connection test failed for '{self.name}': {e}",
                source_type="database",
            )

    def close(self) -> None:
        """Close database connection and dispose engine."""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            logger.info("database_engine_closed", name=self.name)

    def __del__(self) -> None:
        """Cleanup on deletion."""
        self.close()
