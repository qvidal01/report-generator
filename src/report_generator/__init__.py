"""
Report Generator: Multi-source data aggregation and report generation tool.

This package provides tools for pulling data from databases, APIs, and files,
transforming it, and generating reports in various formats (PDF, Excel, HTML).
"""

__version__ = "1.0.0"
__author__ = "AIQSO"
__email__ = "contact@aiqso.io"

from report_generator.core.engine import ReportEngine
from report_generator.datasources.base import DataSource
from report_generator.renderers.template_engine import Template

__all__ = [
    "ReportEngine",
    "DataSource",
    "Template",
    "__version__",
]
