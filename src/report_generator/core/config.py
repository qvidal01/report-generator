"""Report configuration models."""

from typing import Any

from pydantic import BaseModel, Field


class ReportConfig(BaseModel):
    """Configuration for a single report."""

    name: str = Field(description="Report name")
    template: str = Field(description="Template name or path")
    sources: list[dict[str, Any]] = Field(description="List of data source configurations")
    output_format: str = Field(
        default="pdf",
        description="Output format (pdf, excel, html, json)",
    )
    parameters: dict[str, Any] = Field(default_factory=dict, description="Template parameters")
    delivery: dict[str, Any] | None = Field(default=None, description="Delivery configuration")

    class Config:
        """Pydantic config."""

        extra = "allow"
