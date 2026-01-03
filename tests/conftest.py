"""Pytest configuration and shared fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "product": ["Widget A", "Widget B", "Widget C"],
        "sales": [100, 200, 150],
        "revenue": [1000.0, 2000.0, 1500.0],
    })


@pytest.fixture
def sample_template_string() -> str:
    """Create a sample HTML template string."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>{{ title }}</title></head>
    <body>
        <h1>{{ title }}</h1>
        <p>Generated on: {{ date }}</p>
    </body>
    </html>
    """
