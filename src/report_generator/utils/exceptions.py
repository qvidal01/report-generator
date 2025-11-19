"""Custom exception classes for Report Generator."""


class ReportGeneratorError(Exception):
    """Base exception for all Report Generator errors."""

    pass


class ConfigurationError(ReportGeneratorError):
    """Raised when configuration is invalid or missing."""

    pass


class DataSourceError(ReportGeneratorError):
    """Raised when there's an error accessing or processing a data source."""

    def __init__(self, message: str, source_type: str | None = None) -> None:
        """
        Initialize DataSourceError.

        Args:
            message: Error message describing the issue
            source_type: Type of data source (database, api, file)
        """
        super().__init__(message)
        self.source_type = source_type


class TemplateError(ReportGeneratorError):
    """Raised when there's an error with template loading or parsing."""

    def __init__(self, message: str, template_path: str | None = None) -> None:
        """
        Initialize TemplateError.

        Args:
            message: Error message describing the issue
            template_path: Path to the problematic template
        """
        super().__init__(message)
        self.template_path = template_path


class RenderError(ReportGeneratorError):
    """Raised when report rendering fails."""

    def __init__(self, message: str, output_format: str | None = None) -> None:
        """
        Initialize RenderError.

        Args:
            message: Error message describing the issue
            output_format: Format that failed to render (pdf, excel, html)
        """
        super().__init__(message)
        self.output_format = output_format


class DeliveryError(ReportGeneratorError):
    """Raised when report delivery fails."""

    def __init__(self, message: str, delivery_method: str | None = None) -> None:
        """
        Initialize DeliveryError.

        Args:
            message: Error message describing the issue
            delivery_method: Delivery method that failed (email, webhook, storage)
        """
        super().__init__(message)
        self.delivery_method = delivery_method


class ValidationError(ReportGeneratorError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str | None = None) -> None:
        """
        Initialize ValidationError.

        Args:
            message: Error message describing the validation failure
            field: Name of the field that failed validation
        """
        super().__init__(message)
        self.field = field
