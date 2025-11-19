"""API data source implementation."""

from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from report_generator.datasources.base import DataSource
from report_generator.utils.exceptions import DataSourceError
from report_generator.utils.logger import get_logger
from report_generator.utils.validators import validate_url

logger = get_logger(__name__)


class APISource(DataSource):
    """
    Data source for REST APIs.

    Supports GET and POST requests with automatic retries and authentication.
    """

    def __init__(
        self,
        name: str,
        url: str,
        method: str = "GET",
        auth_token: str | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize API source.

        Args:
            name: Name for this data source
            url: API endpoint URL
            method: HTTP method (GET or POST)
            auth_token: Bearer token for authentication
            headers: Additional HTTP headers
            params: Query parameters (for GET requests)
            data: Request body (for POST requests)
            config: Additional configuration (timeout, retries, etc.)
        """
        super().__init__(name, config)
        validate_url(url)
        self.url = url
        self.method = method.upper()
        self.auth_token = auth_token
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or {}

        # Add auth header if token provided
        if self.auth_token:
            self.headers["Authorization"] = f"Bearer {self.auth_token}"

        # Default timeout from config or 30 seconds
        self.timeout = self.config.get("timeout", 30)

    def _get_session(self) -> requests.Session:
        """
        Create requests session with retry logic.

        Returns:
            Configured requests Session
        """
        session = requests.Session()

        # Configure retries for transient failures
        retry_strategy = Retry(
            total=3,  # Total number of retries
            backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def fetch(self) -> pd.DataFrame:
        """
        Fetch data from API and convert to DataFrame.

        Returns:
            DataFrame with API response data

        Raises:
            DataSourceError: If API request fails

        Example:
            >>> source = APISource(
            ...     name="metrics",
            ...     url="https://api.example.com/metrics",
            ...     auth_token="your-token"
            ... )
            >>> df = source.fetch()
        """
        logger.info("fetching_data", source=self.name, url=self.url, method=self.method)

        try:
            session = self._get_session()

            if self.method == "GET":
                response = session.get(
                    self.url,
                    headers=self.headers,
                    params=self.params,
                    timeout=self.timeout,
                )
            elif self.method == "POST":
                response = session.post(
                    self.url,
                    headers=self.headers,
                    json=self.data,
                    timeout=self.timeout,
                )
            else:
                raise DataSourceError(
                    f"Unsupported HTTP method: {self.method}", source_type="api"
                )

            # Raise exception for 4xx/5xx status codes
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Convert to DataFrame (handle different response structures)
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # If dict has a "data" or "results" key, use that
                if "data" in data:
                    df = pd.DataFrame(data["data"])
                elif "results" in data:
                    df = pd.DataFrame(data["results"])
                else:
                    # Convert dict to single-row DataFrame
                    df = pd.DataFrame([data])
            else:
                raise DataSourceError(
                    f"Unexpected API response type: {type(data)}", source_type="api"
                )

            logger.info(
                "data_fetched",
                source=self.name,
                rows=len(df),
                columns=len(df.columns),
                status_code=response.status_code,
            )
            return df

        except requests.exceptions.RequestException as e:
            logger.error("fetch_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"Failed to fetch data from API '{self.name}': {e}", source_type="api"
            )
        except Exception as e:
            logger.error("fetch_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"Failed to process API response from '{self.name}': {e}",
                source_type="api",
            )

    def test_connection(self) -> bool:
        """
        Test API connectivity with a HEAD or GET request.

        Returns:
            True if connection successful

        Raises:
            DataSourceError: If connection fails
        """
        try:
            session = self._get_session()
            # Try HEAD first (lighter), fall back to GET
            try:
                response = session.head(self.url, headers=self.headers, timeout=10)
            except requests.exceptions.RequestException:
                response = session.get(self.url, headers=self.headers, timeout=10)

            response.raise_for_status()
            logger.info("connection_test_passed", source=self.name)
            return True

        except Exception as e:
            logger.error("connection_test_failed", source=self.name, error=str(e))
            raise DataSourceError(
                f"API connection test failed for '{self.name}': {e}", source_type="api"
            )
