"""Tests for configuration module."""

import json
from pathlib import Path

import pytest
import yaml

from report_generator.utils.config import Config, get_config, load_config
from report_generator.utils.exceptions import ConfigurationError


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_yaml_config(self, tmp_path: Path) -> None:
        """Test loading YAML configuration file."""
        config_file = tmp_path / "config.yaml"
        config_data = {"name": "test_report", "template": "default", "format": "pdf"}
        config_file.write_text(yaml.dump(config_data))

        result = load_config(str(config_file))

        assert result["name"] == "test_report"
        assert result["template"] == "default"
        assert result["format"] == "pdf"

    def test_load_yml_config(self, tmp_path: Path) -> None:
        """Test loading .yml configuration file."""
        config_file = tmp_path / "config.yml"
        config_data = {"name": "test_report"}
        config_file.write_text(yaml.dump(config_data))

        result = load_config(str(config_file))

        assert result["name"] == "test_report"

    def test_load_json_config(self, tmp_path: Path) -> None:
        """Test loading JSON configuration file."""
        config_file = tmp_path / "config.json"
        config_data = {"name": "test_report", "output": "report.pdf"}
        config_file.write_text(json.dumps(config_data))

        result = load_config(str(config_file))

        assert result["name"] == "test_report"
        assert result["output"] == "report.pdf"

    def test_load_empty_yaml(self, tmp_path: Path) -> None:
        """Test loading empty YAML file returns empty dict."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")

        result = load_config(str(config_file))

        assert result == {}

    def test_config_file_not_found(self) -> None:
        """Test error when config file doesn't exist."""
        with pytest.raises(ConfigurationError) as exc_info:
            load_config("/nonexistent/config.yaml")

        assert "Configuration file not found" in str(exc_info.value)

    def test_unsupported_config_format(self, tmp_path: Path) -> None:
        """Test error for unsupported configuration format."""
        config_file = tmp_path / "config.txt"
        config_file.write_text("some text")

        with pytest.raises(ConfigurationError) as exc_info:
            load_config(str(config_file))

        assert "Unsupported configuration file format" in str(exc_info.value)

    def test_invalid_yaml_syntax(self, tmp_path: Path) -> None:
        """Test error for invalid YAML syntax."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("invalid: yaml: syntax: [")

        with pytest.raises(ConfigurationError) as exc_info:
            load_config(str(config_file))

        assert "Invalid YAML syntax" in str(exc_info.value)

    def test_invalid_json_syntax(self, tmp_path: Path) -> None:
        """Test error for invalid JSON syntax."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{invalid json}")

        with pytest.raises(ConfigurationError) as exc_info:
            load_config(str(config_file))

        assert "Invalid JSON syntax" in str(exc_info.value)

    def test_load_config_with_path_object(self, tmp_path: Path) -> None:
        """Test loading config with Path object instead of string."""
        config_file = tmp_path / "config.yaml"
        config_data = {"key": "value"}
        config_file.write_text(yaml.dump(config_data))

        result = load_config(config_file)

        assert result["key"] == "value"


class TestConfig:
    """Tests for Config class."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = Config()

        assert config.app_env == "development"
        assert config.log_level == "INFO"
        assert config.smtp_port == 587
        assert config.redis_url == "redis://localhost:6379/0"
        assert config.api_rate_limit == "100/hour"
        assert config.mcp_server_port == 3000

    def test_get_config_function(self) -> None:
        """Test get_config returns Config instance."""
        config = get_config()

        assert isinstance(config, Config)
        assert config.app_env == "development"
