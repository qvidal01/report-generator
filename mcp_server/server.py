"""MCP Server implementation for Report Generator.

This server exposes report generation capabilities via the Model Context Protocol,
allowing AI assistants to generate reports through natural language interactions.
"""

import asyncio
import json
from typing import Any

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, Resource
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: mcp package not installed. Install with: pip install mcp")

from report_generator import ReportEngine, DataSource, Template
from report_generator.utils.logger import get_logger
from report_generator.utils.exceptions import ReportGeneratorError
from report_generator.utils.helpers import generate_id

logger = get_logger(__name__)


class ReportGeneratorMCPServer:
    """MCP Server for Report Generator."""

    def __init__(self) -> None:
        """Initialize MCP server."""
        if not MCP_AVAILABLE:
            raise ImportError(
                "MCP package not installed. Install with: pip install 'report-generator[mcp]'"
            )

        self.server = Server("report-generator")
        self.engine = ReportEngine()
        self._register_tools()
        self._register_resources()
        logger.info("mcp_server_initialized")

    def _register_tools(self) -> None:
        """Register MCP tools."""

        @self.server.tool(
            name="generate_report",
            description="Generate a report from specified data sources and template"
        )
        async def generate_report(
            template: str,
            sources: list[dict[str, Any]],
            output_format: str = "pdf",
            parameters: dict[str, Any] | None = None
        ) -> list[TextContent]:
            """
            Generate a report.

            Args:
                template: Template name or inline template HTML
                sources: List of data source configurations
                output_format: Output format (pdf, excel, html, json)
                parameters: Template variables

            Returns:
                Report generation result
            """
            try:
                logger.info(
                    "mcp_generate_report",
                    template=template[:50],
                    num_sources=len(sources),
                    format=output_format
                )

                # Parse data sources
                data_sources = []
                for source_config in sources:
                    source_type = source_config.get("type")
                    if source_type == "database":
                        ds = DataSource.from_database(
                            connection_string=source_config["connection_string"],
                            query=source_config["query"],
                            name=source_config.get("name", "database")
                        )
                    elif source_type == "api":
                        ds = DataSource.from_api(
                            url=source_config["url"],
                            method=source_config.get("method", "GET"),
                            auth_token=source_config.get("auth_token"),
                            name=source_config.get("name", "api")
                        )
                    elif source_type == "file":
                        ds = DataSource.from_file(
                            file_path=source_config["file_path"],
                            name=source_config.get("name", "file")
                        )
                    else:
                        raise ValueError(f"Unsupported source type: {source_type}")
                    data_sources.append(ds)

                # Create template
                if template.startswith("<") or template.startswith("<!DOCTYPE"):
                    # Inline HTML template
                    tmpl = Template.from_string(template)
                else:
                    # Template file path
                    tmpl = Template.from_file(template)

                # Generate report
                report = self.engine.generate(
                    template=tmpl,
                    sources=data_sources,
                    output_format=output_format,
                    params=parameters or {}
                )

                # Save report
                output_path = f"output/{report.report_id}.{output_format}"
                report.save(output_path)

                return [TextContent(
                    type="text",
                    text=f"Report generated successfully!\n"
                         f"Report ID: {report.report_id}\n"
                         f"Format: {output_format}\n"
                         f"Size: {len(report.content)} bytes\n"
                         f"Saved to: {output_path}"
                )]

            except Exception as e:
                logger.error("mcp_generate_report_failed", error=str(e))
                return [TextContent(
                    type="text",
                    text=f"Error generating report: {str(e)}"
                )]

        @self.server.tool(
            name="list_templates",
            description="List available report templates"
        )
        async def list_templates(category: str | None = None) -> list[TextContent]:
            """
            List available templates.

            Args:
                category: Optional category filter

            Returns:
                List of available templates
            """
            # TODO: Implement template discovery
            templates = [
                {"name": "basic_report", "description": "Basic report template"},
                {"name": "sales_report", "description": "Sales report with charts"},
                {"name": "metrics_dashboard", "description": "Metrics dashboard"},
            ]

            if category:
                templates = [t for t in templates if category.lower() in t["name"].lower()]

            template_list = "\n".join([
                f"- {t['name']}: {t['description']}" for t in templates
            ])

            return [TextContent(
                type="text",
                text=f"Available templates:\n{template_list}"
            )]

        @self.server.tool(
            name="test_datasource",
            description="Test connectivity to a data source"
        )
        async def test_datasource(source_config: dict[str, Any]) -> list[TextContent]:
            """
            Test data source connection.

            Args:
                source_config: Data source configuration

            Returns:
                Connection test result
            """
            try:
                source_type = source_config.get("type")
                if source_type == "database":
                    ds = DataSource.from_database(
                        connection_string=source_config["connection_string"],
                        query="SELECT 1",
                        name="test"
                    )
                elif source_type == "api":
                    ds = DataSource.from_api(
                        url=source_config["url"],
                        auth_token=source_config.get("auth_token"),
                        name="test"
                    )
                elif source_type == "file":
                    ds = DataSource.from_file(
                        file_path=source_config["file_path"],
                        name="test"
                    )
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Unsupported source type: {source_type}"
                    )]

                # Test connection
                success = ds.test_connection()
                return [TextContent(
                    type="text",
                    text=f"✅ Connection successful to {source_type} source!"
                )]

            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Connection failed: {str(e)}"
                )]

    def _register_resources(self) -> None:
        """Register MCP resources."""

        @self.server.resource("report-generator://reports/recent")
        async def get_recent_reports() -> str:
            """Get list of recently generated reports."""
            # TODO: Implement report history tracking
            return json.dumps({
                "reports": [
                    {"id": "rpt_example", "format": "pdf", "created": "2025-11-19"}
                ]
            })

    async def run(self) -> None:
        """Run the MCP server."""
        logger.info("mcp_server_starting")
        await self.server.run()


def main() -> None:
    """Main entry point for MCP server."""
    if not MCP_AVAILABLE:
        print("Error: MCP package not installed.")
        print("Install with: pip install 'report-generator[mcp]'")
        return

    server = ReportGeneratorMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
