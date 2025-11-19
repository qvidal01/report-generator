# API Reference

Complete API documentation for Report Generator.

## Table of Contents

- [Core Classes](#core-classes)
- [Data Sources](#data-sources)
- [Renderers](#renderers)
- [Utilities](#utilities)
- [Configuration](#configuration)
- [Exceptions](#exceptions)

---

## Core Classes

### `ReportEngine`

Main engine for report generation.

**Location:** `report_generator.core.engine`

**Methods:**

#### `__init__(config_path: str | None = None)`

Initialize the report engine.

**Parameters:**
- `config_path` (str, optional): Path to configuration file

**Example:**
```python
engine = ReportEngine(config_path="config.yaml")
```

#### `generate(template, sources, output_format="pdf", params=None) -> Report`

Generate a report from template and data sources.

**Parameters:**
- `template` (Template | str): Template instance or path to template
- `sources` (list[DataSource]): List of data sources
- `output_format` (str): Output format ("pdf", "html", "json", "excel")
- `params` (dict, optional): Template parameters

**Returns:**
- `Report`: Generated report instance

**Raises:**
- `ReportGeneratorError`: If generation fails

**Example:**
```python
report = engine.generate(
    template=Template.from_file("templates/sales.html"),
    sources=[DataSource.from_file("data.csv")],
    output_format="pdf",
    params={"title": "Sales Report"}
)
```

---

### `Report`

Represents a generated report.

**Location:** `report_generator.core.engine`

**Attributes:**
- `report_id` (str): Unique report identifier
- `content` (bytes): Report content
- `output_format` (str): Report format
- `metadata` (dict): Generation metadata

**Methods:**

#### `save(output_path: str | Path) -> None`

Save report to file.

**Example:**
```python
report.save("output/report.pdf")
```

#### `email(to: str, subject: str, body: str | None = None) -> None`

Email the report (planned feature).

#### `upload_to_s3(bucket: str, key: str) -> None`

Upload to S3 (planned feature).

---

## Data Sources

### `DataSource` (Abstract Base)

Base class for all data sources.

**Location:** `report_generator.datasources.base`

**Class Methods:**

#### `from_database(connection_string, query, name="database") -> DatabaseSource`

Create database data source.

**Parameters:**
- `connection_string` (str): SQLAlchemy connection URL
- `query` (str): SQL query to execute
- `name` (str): Data source name

**Example:**
```python
source = DataSource.from_database(
    "postgresql://user:pass@localhost/db",
    "SELECT * FROM orders WHERE date >= '2025-11-01'"
)
```

#### `from_api(url, method="GET", auth_token=None, name="api") -> APISource`

Create API data source.

**Parameters:**
- `url` (str): API endpoint URL
- `method` (str): HTTP method
- `auth_token` (str, optional): Authentication token
- `name` (str): Data source name

**Example:**
```python
source = DataSource.from_api(
    "https://api.example.com/data",
    auth_token="your-token"
)
```

#### `from_file(file_path, name="file") -> FileSource`

Create file data source.

**Parameters:**
- `file_path` (str): Path to CSV, Excel, JSON, or Parquet file
- `name` (str): Data source name

**Example:**
```python
source = DataSource.from_file("data/sales.csv")
```

**Methods:**

#### `fetch() -> pd.DataFrame`

Fetch data from source (abstract method).

**Returns:**
- `pd.DataFrame`: Fetched data

#### `test_connection() -> bool`

Test data source connectivity (abstract method).

**Returns:**
- `bool`: True if connection successful

---

### `DatabaseSource`

SQL database data source.

**Location:** `report_generator.datasources.database`

**Supports:** PostgreSQL, MySQL, SQLite, SQL Server

**Constructor:**
```python
DatabaseSource(
    name: str,
    connection_string: str,
    query: str,
    config: dict | None = None
)
```

**Example:**
```python
source = DatabaseSource(
    name="sales_db",
    connection_string="postgresql://user:pass@localhost/sales",
    query="SELECT * FROM orders WHERE date >= CURRENT_DATE - 7"
)
df = source.fetch()
```

---

### `APISource`

REST API data source.

**Location:** `report_generator.datasources.api`

**Constructor:**
```python
APISource(
    name: str,
    url: str,
    method: str = "GET",
    auth_token: str | None = None,
    headers: dict | None = None,
    params: dict | None = None,
    data: dict | None = None,
    config: dict | None = None
)
```

**Features:**
- Automatic retries with exponential backoff
- Bearer token authentication
- Timeout configuration

**Example:**
```python
source = APISource(
    name="stripe",
    url="https://api.stripe.com/v1/charges",
    auth_token="sk_test_...",
    params={"limit": 100}
)
df = source.fetch()
```

---

### `FileSource`

File-based data source.

**Location:** `report_generator.datasources.file`

**Supported Formats:** CSV, Excel (.xlsx, .xls), JSON, Parquet

**Constructor:**
```python
FileSource(
    name: str,
    file_path: str,
    config: dict | None = None
)
```

**Config Options:**
- `delimiter` (str): CSV delimiter (default: ",")
- `encoding` (str): File encoding (default: "utf-8")
- `sheet_name` (str | int): Excel sheet name/index

**Example:**
```python
source = FileSource(
    name="sales_data",
    file_path="data/sales.csv",
    config={"delimiter": ";", "encoding": "utf-8"}
)
df = source.fetch()
```

---

## Renderers

### `Template`

Template wrapper for Jinja2.

**Location:** `report_generator.renderers.template_engine`

**Class Methods:**

#### `from_file(template_path: str | Path) -> Template`

Load template from file.

**Example:**
```python
template = Template.from_file("templates/report.html")
```

#### `from_string(template_string: str) -> Template`

Create template from string.

**Example:**
```python
template = Template.from_string("<h1>{{ title }}</h1>")
```

**Methods:**

#### `render(context: dict | None = None) -> str`

Render template to HTML.

**Parameters:**
- `context` (dict): Template variables

**Returns:**
- `str`: Rendered HTML

**Example:**
```python
html = template.render({"title": "My Report", "date": "2025-11-19"})
```

#### `render_to_pdf(context: dict | None = None) -> bytes`

Render template to PDF.

**Parameters:**
- `context` (dict): Template variables

**Returns:**
- `bytes`: PDF content

**Requires:** WeasyPrint

**Example:**
```python
pdf_bytes = template.render_to_pdf({"title": "My Report"})
```

---

## Utilities

### Logging

**Location:** `report_generator.utils.logger`

#### `get_logger(name: str) -> structlog.BoundLogger`

Get a structured logger.

**Example:**
```python
from report_generator.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("report_generated", report_id="rpt_123", duration_ms=4500)
```

#### `configure_logging(log_level="INFO", json_logs=False) -> None`

Configure application logging.

**Parameters:**
- `log_level` (str): Log level (DEBUG, INFO, WARNING, ERROR)
- `json_logs` (bool): Enable JSON log output

---

### Validation

**Location:** `report_generator.utils.validators`

#### `validate_email(email: str) -> bool`

Validate email format.

**Raises:** `ValidationError` if invalid

#### `validate_url(url: str) -> bool`

Validate URL format.

**Raises:** `ValidationError` if invalid

#### `validate_cron(cron_expression: str) -> bool`

Validate cron expression.

**Raises:** `ValidationError` if invalid

#### `validate_output_format(format: str) -> bool`

Validate output format.

**Raises:** `ValidationError` if invalid

---

### Helpers

**Location:** `report_generator.utils.helpers`

#### `generate_id(prefix: str = "rpt") -> str`

Generate unique ID.

**Example:**
```python
report_id = generate_id("rpt")  # Returns "rpt_a1b2c3d4"
```

#### `hash_string(value: str) -> str`

Generate SHA256 hash.

#### `format_duration(milliseconds: float) -> str`

Format duration to human-readable string.

#### `format_timestamp(dt: datetime | None = None) -> str`

Format datetime to ISO 8601 string.

---

## Configuration

### `Config`

Application configuration with environment variable support.

**Location:** `report_generator.utils.config`

**Attributes:**
- `app_env` (str): Application environment
- `log_level` (str): Logging level
- `database_url` (str | None): Database connection URL
- `redis_url` (str): Redis connection URL
- `smtp_host` (str | None): SMTP server host
- `smtp_port` (int): SMTP port
- `api_key` (str | None): API authentication key

**Usage:**
```python
from report_generator.utils.config import get_config

config = get_config()
print(config.database_url)
```

### `load_config(config_path: str | Path) -> dict`

Load configuration from YAML or JSON file.

**Example:**
```python
from report_generator.utils.config import load_config

config = load_config("config/report.yaml")
```

---

## Exceptions

**Location:** `report_generator.utils.exceptions`

### `ReportGeneratorError`

Base exception for all errors.

### `ConfigurationError`

Invalid or missing configuration.

### `DataSourceError`

Data source access error.

**Attributes:**
- `source_type` (str): Type of data source

### `TemplateError`

Template loading or parsing error.

**Attributes:**
- `template_path` (str): Path to problematic template

### `RenderError`

Report rendering error.

**Attributes:**
- `output_format` (str): Format that failed

### `DeliveryError`

Report delivery error.

**Attributes:**
- `delivery_method` (str): Method that failed

### `ValidationError`

Input validation error.

**Attributes:**
- `field` (str): Field that failed validation

**Example:**
```python
from report_generator.utils.exceptions import DataSourceError

try:
    df = source.fetch()
except DataSourceError as e:
    print(f"Failed to fetch from {e.source_type}: {e}")
```

---

## Type Hints

Report Generator provides full type hints for all public APIs. Use mypy for type checking:

```bash
mypy your_script.py
```

---

## Version Information

```python
import report_generator
print(report_generator.__version__)  # "1.0.0"
```

---

For more examples and guides, see:
- [README.md](../README.md)
- [Examples](../examples/)
- [MCP Server Guide](MCP_SERVER.md)
