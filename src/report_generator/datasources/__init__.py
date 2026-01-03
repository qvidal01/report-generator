"""Data source connectors for Report Generator."""

from report_generator.datasources.api import APISource
from report_generator.datasources.base import DataSource
from report_generator.datasources.database import DatabaseSource
from report_generator.datasources.file import FileSource

__all__ = [
    "DataSource",
    "DatabaseSource",
    "APISource",
    "FileSource",
]
