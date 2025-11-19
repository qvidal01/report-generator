"""General helper functions."""

import hashlib
import secrets
from datetime import datetime
from typing import Any


def generate_id(prefix: str = "rpt") -> str:
    """
    Generate a unique ID for reports, jobs, etc.

    Args:
        prefix: Prefix for the ID (e.g., "rpt" for reports, "job" for jobs)

    Returns:
        Unique ID string

    Example:
        >>> generate_id("rpt")
        'rpt_a1b2c3d4e5f6'
    """
    random_part = secrets.token_hex(6)
    return f"{prefix}_{random_part}"


def hash_string(value: str) -> str:
    """
    Generate SHA256 hash of a string (useful for cache keys).

    Args:
        value: String to hash

    Returns:
        Hexadecimal hash string

    Example:
        >>> hash_string("SELECT * FROM users")
        '5e884898da...'
    """
    return hashlib.sha256(value.encode()).hexdigest()


def format_duration(milliseconds: float) -> str:
    """
    Format duration in milliseconds to human-readable string.

    Args:
        milliseconds: Duration in milliseconds

    Returns:
        Formatted string (e.g., "1.5s", "500ms")

    Example:
        >>> format_duration(1500)
        '1.50s'
        >>> format_duration(500)
        '500ms'
    """
    if milliseconds < 1000:
        return f"{milliseconds:.0f}ms"
    else:
        seconds = milliseconds / 1000
        return f"{seconds:.2f}s"


def format_timestamp(dt: datetime | None = None) -> str:
    """
    Format datetime to ISO 8601 string.

    Args:
        dt: Datetime to format (defaults to now)

    Returns:
        ISO 8601 formatted string

    Example:
        >>> format_timestamp()
        '2025-11-19T10:30:00Z'
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_get(dictionary: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get value from nested dictionary.

    Args:
        dictionary: Dictionary to search
        key: Key in dot notation (e.g., "user.profile.name")
        default: Default value if key not found

    Returns:
        Value at key or default

    Example:
        >>> data = {"user": {"profile": {"name": "John"}}}
        >>> safe_get(data, "user.profile.name")
        'John'
        >>> safe_get(data, "user.profile.age", 0)
        0
    """
    keys = key.split(".")
    value = dictionary

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value
