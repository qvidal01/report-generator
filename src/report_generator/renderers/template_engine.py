"""Template rendering with Jinja2."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.sandbox import SandboxedEnvironment

from report_generator.utils.exceptions import TemplateError, RenderError
from report_generator.utils.logger import get_logger

logger = get_logger(__name__)


class Template:
    """
    Template wrapper for Jinja2 templates.

    Provides sandboxed template rendering for security.
    """

    def __init__(self, template_string: str | None = None, template_path: Path | None = None) -> None:
        """
        Initialize template.

        Args:
            template_string: Template content as string
            template_path: Path to template file

        Raises:
            TemplateError: If neither template_string nor template_path is provided
        """
        if template_string:
            self.template_string = template_string
            self.template_path = None
        elif template_path:
            self.template_path = Path(template_path)
            if not self.template_path.exists():
                raise TemplateError(
                    f"Template file not found: {template_path}",
                    template_path=str(template_path),
                )
            self.template_string = self.template_path.read_text(encoding="utf-8")
        else:
            raise TemplateError("Either template_string or template_path must be provided")

        # Use sandboxed environment for security
        self.env = SandboxedEnvironment(
            autoescape=select_autoescape(["html", "xml"]),
        )

        try:
            self.template = self.env.from_string(self.template_string)
        except Exception as e:
            raise TemplateError(f"Failed to parse template: {e}", template_path=str(template_path) if template_path else None)

    @classmethod
    def from_file(cls, template_path: str | Path) -> "Template":
        """
        Load template from file.

        Args:
            template_path: Path to template file

        Returns:
            Template instance

        Example:
            >>> template = Template.from_file("templates/sales_report.html")
        """
        return cls(template_path=Path(template_path))

    @classmethod
    def from_string(cls, template_string: str) -> "Template":
        """
        Create template from string.

        Args:
            template_string: Template content

        Returns:
            Template instance

        Example:
            >>> template = Template.from_string("<h1>{{ title }}</h1>")
        """
        return cls(template_string=template_string)

    def render(self, context: dict[str, Any] | None = None) -> str:
        """
        Render template to HTML string.

        Args:
            context: Variables to pass to template

        Returns:
            Rendered HTML string

        Raises:
            RenderError: If rendering fails

        Example:
            >>> template = Template.from_string("<h1>{{ title }}</h1>")
            >>> html = template.render({"title": "My Report"})
        """
        context = context or {}
        logger.info("rendering_template", variables=list(context.keys()))

        try:
            html = self.template.render(**context)
            logger.info("template_rendered", html_length=len(html))
            return html
        except Exception as e:
            logger.error("template_render_failed", error=str(e))
            raise RenderError(f"Failed to render template: {e}")

    def render_to_pdf(self, context: dict[str, Any] | None = None) -> bytes:
        """
        Render template to PDF bytes.

        Args:
            context: Variables to pass to template

        Returns:
            PDF content as bytes

        Raises:
            RenderError: If PDF generation fails

        Example:
            >>> template = Template.from_file("templates/report.html")
            >>> pdf_bytes = template.render_to_pdf({"title": "Report"})
        """
        html = self.render(context)

        try:
            from weasyprint import HTML

            logger.info("generating_pdf", html_length=len(html))
            pdf_bytes = HTML(string=html).write_pdf()
            logger.info("pdf_generated", pdf_size_bytes=len(pdf_bytes))
            return pdf_bytes
        except ImportError:
            raise RenderError(
                "WeasyPrint not installed. Install with: pip install weasyprint",
                output_format="pdf",
            )
        except Exception as e:
            logger.error("pdf_generation_failed", error=str(e))
            raise RenderError(f"Failed to generate PDF: {e}", output_format="pdf")
