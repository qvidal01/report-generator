"""Tests for template rendering."""

import pytest

from report_generator.renderers.template_engine import Template
from report_generator.utils.exceptions import TemplateError


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
