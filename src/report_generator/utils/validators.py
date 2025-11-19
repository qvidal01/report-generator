"""Input validation utilities."""

import re
from typing import Any
from urllib.parse import urlparse

from report_generator.utils.exceptions import ValidationError


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If email format is invalid

    Example:
        >>> validate_email("user@example.com")
        True
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValidationError(f"Invalid email address: {email}", field="email")
    return True


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If URL format is invalid

    Example:
        >>> validate_url("https://api.example.com/data")
        True
    """
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValidationError(f"Invalid URL format: {url}", field="url")
        if result.scheme not in ["http", "https", "ftp", "ftps"]:
            raise ValidationError(
                f"Unsupported URL scheme: {result.scheme}", field="url"
            )
        return True
    except Exception as e:
        raise ValidationError(f"Invalid URL: {url} - {e}", field="url")


def validate_cron(cron_expression: str) -> bool:
    """
    Validate cron expression format (basic validation).

    Args:
        cron_expression: Cron expression to validate (e.g., "0 9 * * *")

    Returns:
        True if valid format

    Raises:
        ValidationError: If cron expression format is invalid

    Example:
        >>> validate_cron("0 9 * * *")
        True
        >>> validate_cron("0 9 * * MON")
        True
    """
    parts = cron_expression.split()
    if len(parts) not in [5, 6]:  # 5 for standard, 6 with seconds
        raise ValidationError(
            f"Cron expression must have 5 or 6 parts, got {len(parts)}",
            field="cron",
        )

    # Basic validation of each part
    for i, part in enumerate(parts):
        # Allow numbers, ranges, wildcards, steps, and day names
        if not re.match(r"^[\d\-\*\/,A-Z]+$", part):
            raise ValidationError(
                f"Invalid cron expression part: {part}", field="cron"
            )

    return True


def validate_output_format(format: str) -> bool:
    """
    Validate output format.

    Args:
        format: Output format (pdf, excel, html, json)

    Returns:
        True if valid

    Raises:
        ValidationError: If format is not supported

    Example:
        >>> validate_output_format("pdf")
        True
    """
    valid_formats = ["pdf", "excel", "html", "json"]
    if format.lower() not in valid_formats:
        raise ValidationError(
            f"Invalid output format: {format}. Must be one of {valid_formats}",
            field="output_format",
        )
    return True
