# 📊 Report Generator

[![CI](https://github.com/qvidal01/report-generator/workflows/CI/badge.svg)](https://github.com/qvidal01/report-generator/actions)
[![codecov](https://codecov.io/gh/qvidal01/report-generator/branch/main/graph/badge.svg)](https://codecov.io/gh/qvidal01/report-generator)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Multi-source data aggregation and report generation tool. Pull data from databases, REST APIs, and files to create beautiful, automated reports in PDF, Excel, and HTML formats.

## ✨ Features

- **🔌 Multi-Source Connectivity** - Connect to PostgreSQL, MySQL, MongoDB, REST APIs, CSV, Excel, and more
- **🎨 Customizable Templates** - Design reports with Jinja2 templates and custom CSS styling
- **📅 Automated Scheduling** - Generate reports on a schedule with cron expressions
- **📧 Smart Delivery** - Email, webhook, or S3 delivery with automatic retries
- **📊 Rich Visualizations** - Create charts and graphs with Plotly
- **🚀 REST API** - Programmatic access with FastAPI and automatic OpenAPI docs
- **⚡ High Performance** - Async data fetching, caching, and parallel processing
- **🔒 Security First** - Environment-based secrets, input validation, sandboxed templates
- **🤖 MCP Server** - Integrate with AI assistants via Model Context Protocol

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [CLI](#cli)
  - [Python API](#python-api)
  - [REST API](#rest-api)
- [Examples](#-examples)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

```bash
# Install from PyPI (coming soon)
pip install report-generator

# Or install from source
git clone https://github.com/qvidal01/report-generator.git
cd report-generator
pip install -e ".[dev]"

# Set up configuration
cp .env.example .env
# Edit .env with your credentials

# Generate your first report
report-generator generate examples/sales_report.yaml

# Start the API server
report-generator serve --port 8080
```

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Redis (optional, for caching)
- PostgreSQL/MySQL (optional, for database sources)

### Basic Installation

```bash
pip install report-generator
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/qvidal01/report-generator.git
cd report-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Optional Dependencies

```bash
# MCP server support
pip install "report-generator[mcp]"

# Celery for distributed task processing
pip install "report-generator[celery]"

# Monitoring and observability
pip install "report-generator[monitoring]"
```

## ⚙️ Configuration

Create a `.env` file with your credentials:

```bash
# Copy example configuration
cp .env.example .env

# Edit with your settings
nano .env
```

Example `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/reports

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# API
API_KEY=your-secret-api-key
```

## 📖 Usage

### CLI

```bash
# Generate a report from config file
report-generator generate config/sales_report.yaml --output report.pdf

# Schedule a recurring report
report-generator schedule config/daily_metrics.yaml --cron "0 9 * * *"

# List scheduled reports
report-generator schedule list

# Test data source connection
report-generator datasource test config/postgres_config.yaml

# Start API server
report-generator serve --host 0.0.0.0 --port 8080

# Validate configuration
report-generator validate config/report.yaml

# Show version
report-generator --version
```

### Python API

```python
from report_generator import ReportEngine, DataSource, Template

# Initialize engine
engine = ReportEngine(config_path="config.yaml")

# Define data sources
db_source = DataSource.from_database(
    connection_string="postgresql://user:pass@localhost/sales",
    query="SELECT * FROM orders WHERE date >= CURRENT_DATE - INTERVAL '7 days'"
)

api_source = DataSource.from_api(
    url="https://api.example.com/metrics",
    auth_token="your-token"
)

# Load template
template = Template.from_file("templates/weekly_sales.html")

# Generate report
report = engine.generate(
    template=template,
    sources=[db_source, api_source],
    output_format="pdf",
    params={"title": "Weekly Sales Report", "date": "2025-11-19"}
)

# Save or deliver
report.save("output/weekly_sales.pdf")
report.email(to="team@example.com", subject="Weekly Report")
report.upload_to_s3(bucket="reports", key="weekly_sales.pdf")
```

### REST API

Start the server:

```bash
report-generator serve --port 8080
```

API endpoints:

```http
# Generate a report
POST /api/v1/reports/generate
Content-Type: application/json
X-API-Key: your-api-key

{
  "template": "sales_report",
  "sources": [
    {
      "type": "database",
      "config": {
        "query": "SELECT * FROM sales WHERE date >= '2025-11-01'"
      }
    }
  ],
  "output_format": "pdf",
  "parameters": {
    "title": "November Sales"
  }
}

# Get report status
GET /api/v1/reports/{report_id}

# Download report
GET /api/v1/reports/{report_id}/download

# List schedules
GET /api/v1/schedules

# Health check
GET /health
```

Interactive API docs available at `http://localhost:8080/docs`

## 📚 Examples

See the [`examples/`](./examples) directory for complete examples:

- **[basic_report.py](./examples/basic_report.py)** - Simple report from a single data source
- **[multi_source_report.py](./examples/multi_source_report.py)** - Combining data from multiple sources
- **[scheduled_report.py](./examples/scheduled_report.py)** - Setting up automated report generation
- **[custom_template.py](./examples/custom_template.py)** - Creating custom templates with charts
- **[api_usage.py](./examples/api_usage.py)** - Using the REST API programmatically

## 📘 Documentation

- **[ANALYSIS_SUMMARY.md](./ANALYSIS_SUMMARY.md)** - Architecture and design decisions
- **[ISSUES_FOUND.md](./ISSUES_FOUND.md)** - Known issues and limitations
- **[IMPROVEMENT_PLAN.md](./IMPROVEMENT_PLAN.md)** - Roadmap and future enhancements
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - How to contribute
- **[docs/API_REFERENCE.md](./docs/API_REFERENCE.md)** - Complete API documentation
- **[docs/MCP_SERVER.md](./docs/MCP_SERVER.md)** - MCP server setup and usage

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Report Generator                    │
├─────────────────────────────────────────────────┤
│  CLI │ REST API │ Python Library │ MCP Server   │
└──────┬─────────────────────────────────┬────────┘
       │        Core Engine              │
       ├─────────────────────────────────┤
       │ Data Sources │ Processors │ Renderers │
       └─────────────────────────────────┘
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=report_generator --cov-report=html

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Slow tests

# Run linting and type checking
black --check .
ruff check .
mypy src/
```

## 🐳 Docker

```bash
# Build image
docker build -t report-generator .

# Run with docker-compose (includes Redis and PostgreSQL)
docker-compose up -d

# Run API server
docker run -p 8080:8080 --env-file .env report-generator

# Run CLI command
docker run --env-file .env report-generator report-generator --version
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

Quick checklist:
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes with tests
- Run tests and linting (`pytest && black . && ruff check .`)
- Commit with descriptive message (`git commit -m 'feat: add amazing feature'`)
- Push to your fork (`git push origin feature/amazing-feature`)
- Open a Pull Request

See [good first issues](https://github.com/qvidal01/report-generator/labels/good%20first%20issue) for ideas!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/), [Pandas](https://pandas.pydata.org/), and [WeasyPrint](https://weasyprint.org/)
- Inspired by modern data engineering tools and practices
- Thanks to all [contributors](https://github.com/qvidal01/report-generator/graphs/contributors)

## 📞 Support

- 📫 **Issues:** [GitHub Issues](https://github.com/qvidal01/report-generator/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/qvidal01/report-generator/discussions)
- 🌐 **Website:** [aiqso.io](https://aiqso.io)

---

Made with ❤️ by [AIQSO](https://aiqso.io)
