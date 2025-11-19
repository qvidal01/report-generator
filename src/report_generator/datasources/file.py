"""File data source implementation."""

from pathlib import Path
from typing import Any

import pandas as pd

from report_generator.datasources.base import DataSource
from report_generator.utils.exceptions import DataSourceError
from report_generator.utils.logger import get_logger

logger = get_logger(__name__)


class FileSource(DataSource):
    """
    Data source for files (CSV, Excel, JSON, Parquet).

    Automatically detects file format based on extension.
    """

    def __init__(
        self, name: str, file_path: str, config: dict[str, Any] | None = None
    ) -> None:
        """
        Initialize file source.

        Args:
            name: Name for this data source
            file_path: Path to data file (.csv, .xlsx, .json, .parquet)
            config: Additional configuration (e.g., CSV delimiter, Excel sheet name)
        """
        super().__init__(name, config)
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise DataSourceError(
                f"File not found: {file_path}", source_type="file"
            )

    def fetch(self) -> pd.DataFrame:
        """
        Read file and return DataFrame.

        Returns:
            DataFrame with file contents

        Raises:
            DataSourceError: If file reading fails

        Example:
            >>> source = FileSource(name="sales", file_path="data/sales.csv")
            >>> df = source.fetch()
        """
        logger.info(
            "fetching_data",
            source=self.name,
            file_path=str(self.file_path),
            file_type=self.file_path.suffix,
        )

        try:
            suffix = self.file_path.suffix.lower()

            if suffix == ".csv":
                df = pd.read_csv(
                    self.file_path,
                    delimiter=self.config.get("delimiter", ","),
                    encoding=self.config.get("encoding", "utf-8"),
                )
            elif suffix in [".xlsx", ".xls"]:
                df = pd.read_excel(
                    self.file_path,
                    sheet_name=self.config.get("sheet_name", 0),
                )
            elif suffix == ".json":
                df = pd.read_json(
                    self.file_path,
                    orient=self.config.get("orient", "records"),
                )
            elif suffix == ".parquet":
                df = pd.read_parquet(self.file_path)
            else:
                raise DataSourceError(
                    f"Unsupported file format: {suffix}. "
                    "Supported formats: .csv, .xlsx, .xls, .json, .parquet",
                    source_type="file",
                )

            logger.info(
                "data_fetched",
                source=self.name,
                rows=len(df),
                columns=len(df.columns),
            )
            return df

        except Exception as e:
            logger.error("fetch_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"Failed to read file '{self.name}': {e}", source_type="file"
            )

    def test_connection(self) -> bool:
        """
        Test if file exists and is readable.

        Returns:
            True if file is accessible
        """
        try:
            if not self.file_path.exists():
                raise FileNotFoundError(f"File not found: {self.file_path}")

            # Try to read first few rows to verify format
            suffix = self.file_path.suffix.lower()
            if suffix == ".csv":
                pd.read_csv(self.file_path, nrows=1)
            elif suffix in [".xlsx", ".xls"]:
                pd.read_excel(self.file_path, nrows=1)
            elif suffix == ".json":
                pd.read_json(self.file_path, lines=True, nrows=1)
            elif suffix == ".parquet":
                pd.read_parquet(self.file_path)

            logger.info("connection_test_passed", source=self.name)
            return True

        except Exception as e:
            logger.error("connection_test_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"File connection test failed for '{self.name}': {e}",
                source_type="file",
            )
