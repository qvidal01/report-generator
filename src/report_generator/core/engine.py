"""Core report generation engine."""

import time
from pathlib import Path
from typing import Any

import pandas as pd

from report_generator.datasources.base import DataSource
from report_generator.renderers.template_engine import Template
from report_generator.utils.exceptions import ReportGeneratorError
from report_generator.utils.helpers import generate_id, format_duration
from report_generator.utils.logger import get_logger

logger = get_logger(__name__)


class Report:
    """
    Represents a generated report.

    Provides methods for saving and delivering the report.
    """

    def __init__(
        self,
        report_id: str,
        content: bytes,
        output_format: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize report.

        Args:
            report_id: Unique report identifier
            content: Report content as bytes
            output_format: Format of the report (pdf, excel, html)
            metadata: Additional metadata (generation time, sources, etc.)
        """
        self.report_id = report_id
        self.content = content
        self.output_format = output_format
        self.metadata = metadata or {}

    def save(self, output_path: str | Path) -> None:
        """
        Save report to file.

        Args:
            output_path: Path where report should be saved

        Example:
            >>> report.save("output/weekly_report.pdf")
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(self.content)

        logger.info(
            "report_saved",
            report_id=self.report_id,
            path=str(output_path),
            size_bytes=len(self.content),
        )

    def email(self, to: str, subject: str, body: str | None = None) -> None:
        """
        Email the report (placeholder for future implementation).

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
        """
        logger.info("report_email_placeholder", report_id=self.report_id, to=to)
        # TODO: Implement email delivery
        raise NotImplementedError("Email delivery not yet implemented")

    def upload_to_s3(self, bucket: str, key: str) -> None:
        """
        Upload report to S3 (placeholder for future implementation).

        Args:
            bucket: S3 bucket name
            key: S3 object key
        """
        logger.info("report_s3_upload_placeholder", report_id=self.report_id, bucket=bucket)
        # TODO: Implement S3 upload
        raise NotImplementedError("S3 upload not yet implemented")


class ReportEngine:
    """
    Main engine for report generation.

    Orchestrates data fetching, transformation, and rendering.
    """

    def __init__(self, config_path: str | None = None) -> None:
        """
        Initialize report engine.

        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path
        logger.info("report_engine_initialized", config_path=config_path)

    def generate(
        self,
        template: Template | str,
        sources: list[DataSource],
        output_format: str = "pdf",
        params: dict[str, Any] | None = None,
    ) -> Report:
        """
        Generate a report from template and data sources.

        Args:
            template: Template instance or path to template file
            sources: List of data sources to fetch data from
            output_format: Output format (pdf, excel, html, json)
            params: Template parameters/variables

        Returns:
            Generated Report instance

        Raises:
            ReportGeneratorError: If report generation fails

        Example:
            >>> engine = ReportEngine()
            >>> template = Template.from_file("templates/sales.html")
            >>> sources = [DataSource.from_file("data/sales.csv")]
            >>> report = engine.generate(template, sources, output_format="pdf")
            >>> report.save("output/sales_report.pdf")
        """
        report_id = generate_id("rpt")
        start_time = time.time()

        logger.info(
            "report_generation_started",
            report_id=report_id,
            num_sources=len(sources),
            output_format=output_format,
        )

        try:
            # Step 1: Fetch data from all sources
            data_frames = {}
            for i, source in enumerate(sources):
                logger.info("fetching_source", report_id=report_id, source=source.name)
                df = source.fetch()
                # Use source name as key, or default to index
                key = source.name if source.name else f"source_{i}"
                data_frames[key] = df

            # Step 2: Combine data (simple concatenation for now)
            if len(data_frames) == 1:
                combined_data = list(data_frames.values())[0]
            else:
                # For multiple sources, make them available as dict
                combined_data = data_frames

            # Step 3: Load template if string path provided
            if isinstance(template, str):
                template = Template.from_file(template)

            # Step 4: Render template with data
            params = params or {}
            params["data"] = combined_data  # Make data available in template

            if output_format == "html":
                html_content = template.render(params)
                content = html_content.encode("utf-8")
            elif output_format == "pdf":
                content = template.render_to_pdf(params)
            elif output_format == "json":
                # For JSON, just export the data
                if isinstance(combined_data, pd.DataFrame):
                    content = combined_data.to_json(orient="records").encode("utf-8")
                else:
                    import json
                    content = json.dumps(combined_data, indent=2).encode("utf-8")
            else:
                raise ReportGeneratorError(f"Unsupported output format: {output_format}")

            # Step 5: Create report object
            duration_ms = (time.time() - start_time) * 1000
            metadata = {
                "report_id": report_id,
                "sources": [s.name for s in sources],
                "output_format": output_format,
                "generation_time_ms": duration_ms,
                "size_bytes": len(content),
            }

            report = Report(
                report_id=report_id,
                content=content,
                output_format=output_format,
                metadata=metadata,
            )

            logger.info(
                "report_generation_completed",
                report_id=report_id,
                duration=format_duration(duration_ms),
                size_bytes=len(content),
            )

            return report

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                "report_generation_failed",
                report_id=report_id,
                error=str(e),
                duration=format_duration(duration_ms),
            )
            raise ReportGeneratorError(f"Report generation failed: {e}")
