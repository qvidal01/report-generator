"""Configuration management for Report Generator."""

import json
import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from report_generator.utils.exceptions import ConfigurationError


class Config(BaseSettings):
    """
    Application configuration with environment variable support.

    Configuration can be loaded from:
    1. Environment variables (highest priority)
    2. .env file
    3. Default values (lowest priority)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Application settings
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    secret_key: str = Field(default="change-me-in-production", description="Secret key")

    # Database
    database_url: str | None = Field(default=None, description="Database connection URL")

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    # Email/SMTP
    smtp_host: str | None = Field(default=None, description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_username: str | None = Field(default=None, description="SMTP username")
    smtp_password: str | None = Field(default=None, description="SMTP password")
    smtp_from: str = Field(default="reports@example.com", description="From email address")

    # API
    api_key: str | None = Field(default=None, description="API authentication key")
    api_rate_limit: str = Field(default="100/hour", description="API rate limit")

    # MCP Server
    mcp_server_port: int = Field(default=3000, description="MCP server port")


def load_config(config_path: str | Path) -> dict[str, Any]:
    """
    Load configuration from a YAML or JSON file.

    Args:
        config_path: Path to configuration file (.yaml, .yml, or .json)

    Returns:
        Configuration dictionary

    Raises:
        ConfigurationError: If file doesn't exist or has invalid format

    Example:
        >>> config = load_config("config/report.yaml")
        >>> print(config["template"])
    """
    path = Path(config_path)

    if not path.exists():
        raise ConfigurationError(f"Configuration file not found: {config_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f) or {}
            elif path.suffix == ".json":
                return json.load(f)
            else:
                raise ConfigurationError(
                    f"Unsupported configuration file format: {path.suffix}. "
                    "Use .yaml, .yml, or .json"
                )
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML syntax in {config_path}: {e}")
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON syntax in {config_path}: {e}")
    except Exception as e:
        raise ConfigurationError(f"Error loading configuration from {config_path}: {e}")


def get_config() -> Config:
    """
    Get the application configuration.

    Returns:
        Config instance with values from environment variables and .env file

    Example:
        >>> config = get_config()
        >>> print(config.database_url)
    """
    return Config()
