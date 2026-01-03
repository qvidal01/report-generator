"""Tests for utility functions."""

import pytest

from report_generator.utils.exceptions import ValidationError
from report_generator.utils.helpers import format_duration, generate_id, hash_string
from report_generator.utils.validators import (
    validate_cron,
    validate_email,
    validate_output_format,
    validate_url,
)


class TestValidators:
    """Test validation functions."""

    def test_validate_email_valid(self) -> None:
        """Test valid email addresses."""
        assert validate_email("user@example.com") is True
        assert validate_email("test.user+tag@domain.co.uk") is True

    def test_validate_email_invalid(self) -> None:
        """Test invalid email addresses."""
        with pytest.raises(ValidationError):
            validate_email("invalid-email")
        with pytest.raises(ValidationError):
            validate_email("@example.com")

    def test_validate_url_valid(self) -> None:
        """Test valid URLs."""
        assert validate_url("https://example.com") is True
        assert validate_url("http://api.example.com/data") is True

    def test_validate_url_invalid(self) -> None:
        """Test invalid URLs."""
        with pytest.raises(ValidationError):
            validate_url("not-a-url")
        with pytest.raises(ValidationError):
            validate_url("://missing-scheme.com")

    def test_validate_cron_valid(self) -> None:
        """Test valid cron expressions."""
        assert validate_cron("0 9 * * *") is True
        assert validate_cron("*/15 * * * *") is True
        assert validate_cron("0 0 * * MON") is True

    def test_validate_cron_invalid(self) -> None:
        """Test invalid cron expressions."""
        with pytest.raises(ValidationError):
            validate_cron("invalid")
        with pytest.raises(ValidationError):
            validate_cron("0 9 *")  # Too few parts

    def test_validate_output_format(self) -> None:
        """Test output format validation."""
        assert validate_output_format("pdf") is True
        assert validate_output_format("excel") is True
        with pytest.raises(ValidationError):
            validate_output_format("invalid")


class TestHelpers:
    """Test helper functions."""

    def test_generate_id(self) -> None:
        """Test ID generation."""
        id1 = generate_id("rpt")
        id2 = generate_id("rpt")

        assert id1.startswith("rpt_")
        assert id2.startswith("rpt_")
        assert id1 != id2  # Should be unique

    def test_hash_string(self) -> None:
        """Test string hashing."""
        hash1 = hash_string("test")
        hash2 = hash_string("test")
        hash3 = hash_string("different")

        assert hash1 == hash2  # Same input = same hash
        assert hash1 != hash3  # Different input = different hash
        assert len(hash1) == 64  # SHA256 produces 64-char hex

    def test_format_duration(self) -> None:
        """Test duration formatting."""
        assert format_duration(500) == "500ms"
        assert format_duration(1500) == "1.50s"
        assert format_duration(1000) == "1.00s"
