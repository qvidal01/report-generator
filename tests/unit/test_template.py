"""Tests for template rendering."""

from pathlib import Path

import pytest

from report_generator.renderers.template_engine import Template
from report_generator.utils.exceptions import RenderError, TemplateError


class TestTemplate:
    """Test template rendering."""

    def test_create_from_string(self, sample_template_string: str) -> None:
        """Test creating template from string."""
        template = Template.from_string(sample_template_string)
        assert template is not None
        assert template.template_string == sample_template_string

    def test_render_template(self, sample_template_string: str) -> None:
        """Test rendering template with context."""
        template = Template.from_string(sample_template_string)
        html = template.render({"title": "Test Report", "date": "2025-11-19"})

        assert "Test Report" in html
        assert "2025-11-19" in html

    def test_render_missing_variable(self, sample_template_string: str) -> None:
        """Test rendering with missing variable."""
        template = Template.from_string(sample_template_string)
        # Should not raise, missing variables are empty in Jinja2
        html = template.render({"title": "Test"})
        assert "Test" in html

    def test_invalid_template_syntax(self) -> None:
        """Test template with invalid syntax."""
        with pytest.raises(TemplateError):
            Template.from_string("{{ unclosed")

    def test_create_from_file(self, tmp_path: Path) -> None:
        """Test creating template from file."""
        template_file = tmp_path / "template.html"
        template_file.write_text("<h1>{{ title }}</h1>")

        template = Template.from_file(template_file)

        assert template is not None
        assert template.template_path == template_file

    def test_create_from_file_not_found(self) -> None:
        """Test error when template file not found."""
        with pytest.raises(TemplateError) as exc_info:
            Template.from_file("/nonexistent/template.html")

        assert "Template file not found" in str(exc_info.value)

    def test_create_without_string_or_path(self) -> None:
        """Test error when neither string nor path provided."""
        with pytest.raises(TemplateError) as exc_info:
            Template()

        assert "Either template_string or template_path must be provided" in str(exc_info.value)

    def test_render_with_no_context(self) -> None:
        """Test rendering template with no context (None)."""
        template = Template.from_string("<p>Static content</p>")
        html = template.render(None)

        assert "Static content" in html

    def test_render_with_empty_context(self) -> None:
        """Test rendering template with empty context dict."""
        template = Template.from_string("<p>Static content</p>")
        html = template.render({})

        assert "Static content" in html

    def test_render_to_pdf(self, sample_template_string: str) -> None:
        """Test rendering template to PDF."""
        template = Template.from_string(sample_template_string)
        pdf_bytes = template.render_to_pdf({"title": "PDF Report", "date": "2025-11-19"})

        # PDF files start with %PDF
        assert pdf_bytes[:4] == b"%PDF"
        assert len(pdf_bytes) > 0

    def test_render_to_pdf_with_no_context(self) -> None:
        """Test rendering to PDF with no context."""
        template = Template.from_string("<h1>Static PDF</h1>")
        pdf_bytes = template.render_to_pdf()

        assert pdf_bytes[:4] == b"%PDF"

    def test_render_complex_template(self) -> None:
        """Test rendering complex template with loops and conditionals."""
        template_str = """
        <ul>
        {% for item in items %}
            <li>{{ item.name }}: ${{ item.price }}</li>
        {% endfor %}
        </ul>
        {% if show_total %}
        <p>Total items: {{ items|length }}</p>
        {% endif %}
        """
        template = Template.from_string(template_str)
        context = {
            "items": [
                {"name": "Widget", "price": 10},
                {"name": "Gadget", "price": 20},
            ],
            "show_total": True,
        }
        html = template.render(context)

        assert "Widget: $10" in html
        assert "Gadget: $20" in html
        assert "Total items: 2" in html
