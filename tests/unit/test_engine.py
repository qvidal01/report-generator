"""Tests for report generation engine."""

import json
from typing import Any

import pandas as pd

from report_generator.core.engine import ReportEngine
from report_generator.datasources.base import DataSource
from report_generator.renderers.template_engine import Template


class DummySource(DataSource):
    """Simple in-memory data source for testing."""

    def __init__(self, name: str, dataframe: pd.DataFrame) -> None:
        super().__init__(name=name)
        self._dataframe = dataframe

    def fetch(self) -> pd.DataFrame:
        return self._dataframe

    def test_connection(self) -> bool:
        return True


class TestReportEngine:
    """Test cases for the report engine."""

    def test_generate_json_multi_source(self, sample_dataframe: pd.DataFrame) -> None:
        """Ensure JSON export supports multiple sources."""
        engine = ReportEngine()
        template = Template.from_string("<div>{{ data }}</div>")

        other_df = sample_dataframe[["product", "sales"]].copy()
        source_a = DummySource("sales", sample_dataframe)
        source_b = DummySource("summary", other_df)

        report = engine.generate(
            template=template,
            sources=[source_a, source_b],
            output_format="json",
        )

        payload: dict[str, Any] = json.loads(report.content.decode("utf-8"))
        assert "sales" in payload
        assert "summary" in payload
        assert len(payload["sales"]) == len(sample_dataframe)
        assert len(payload["summary"]) == len(other_df)

    def test_generate_excel_single_source(
        self,
        sample_dataframe: pd.DataFrame,
        tmp_path: Any,
    ) -> None:
        """Ensure Excel export writes valid workbooks."""
        engine = ReportEngine()
        template = Template.from_string("<div>{{ data }}</div>")
        source = DummySource("sales", sample_dataframe)

        report = engine.generate(
            template=template,
            sources=[source],
            output_format="excel",
        )

        output_file = tmp_path / "report.xlsx"
        report.save(output_file)

        exported = pd.read_excel(output_file)
        assert list(exported.columns) == list(sample_dataframe.columns)
        assert len(exported) == len(sample_dataframe)
