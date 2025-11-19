# Analysis Summary: Report Generator

## Purpose & Problem Statement

**Problem:** Organizations often need to aggregate data from multiple disparate sources (databases, REST APIs, CSV files, spreadsheets) and generate formatted reports for stakeholders. Existing solutions are either too expensive, too complex, or lack flexibility in data source integration.

**Solution:** Report Generator is a Python-based tool that provides a unified interface for connecting to multiple data sources, transforming data, and generating reports in various formats (PDF, Excel, HTML). It enables both interactive and scheduled report generation with minimal configuration.

**Target Users:**
- Data analysts who need to automate recurring reports
- DevOps teams monitoring system metrics from multiple sources
- Business intelligence teams creating executive dashboards
- Small-to-medium businesses without expensive BI infrastructure

## Core Features

### 1. Multi-Source Data Connectivity
- **Database Support:** PostgreSQL, MySQL, SQLite, MongoDB
- **API Integration:** REST APIs with OAuth/API key authentication
- **File Sources:** CSV, Excel, JSON, Parquet
- **Cloud Storage:** S3, Google Cloud Storage (planned)

### 2. Data Transformation Pipeline
- SQL-like query language for filtering and aggregation
- Pandas-based transformations for complex operations
- Data validation and quality checks
- Caching layer for performance optimization

### 3. Report Generation
- **Templates:** Jinja2-based customizable templates
- **Output Formats:** PDF (via WeasyPrint), Excel (via openpyxl), HTML, JSON
- **Visualization:** Charts via Plotly or Matplotlib
- **Styling:** CSS support for branded reports

### 4. Scheduling & Automation
- Cron-style scheduling for recurring reports
- Event-triggered generation (webhook support)
- Email delivery integration (SMTP)
- Slack/Teams notification support

### 5. API & Web Interface
- RESTful API for programmatic access
- Simple web dashboard for configuration
- CLI for local execution and testing

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Report Generator                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CLI Tool   │    │   REST API   │    │ Web Dashboard│  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │            │
│         └───────────────────┴───────────────────┘            │
│                             │                                │
│                   ┌─────────▼─────────┐                      │
│                   │  Core Engine      │                      │
│                   │  - Job Scheduler  │                      │
│                   │  - Config Manager │                      │
│                   └─────────┬─────────┘                      │
│                             │                                │
│         ┌───────────────────┼───────────────────┐            │
│         │                   │                   │            │
│  ┌──────▼───────┐  ┌────────▼────────┐  ┌──────▼───────┐   │
│  │ Data Sources │  │ Data Processor  │  │   Renderer   │   │
│  │  - Database  │  │ - Transformers  │  │  - Templates │   │
│  │  - API       │  │ - Validators    │  │  - Exporters │   │
│  │  - Files     │  │ - Cache         │  │  - Formatters│   │
│  └──────────────┘  └─────────────────┘  └──────┬───────┘   │
│                                                 │            │
│                                         ┌───────▼───────┐   │
│                                         │   Delivery    │   │
│                                         │  - Email      │   │
│                                         │  - Webhooks   │   │
│                                         │  - Storage    │   │
│                                         └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Module Breakdown

**src/core/**
- `engine.py` - Main orchestration and job execution
- `scheduler.py` - Cron-based task scheduling
- `config.py` - Configuration management (YAML/JSON)

**src/datasources/**
- `base.py` - Abstract base class for data sources
- `database.py` - Database connectors (SQLAlchemy)
- `api.py` - REST API client with retry logic
- `file.py` - File readers (CSV, Excel, JSON)

**src/processors/**
- `transformer.py` - Data transformation logic
- `validator.py` - Data quality checks
- `cache.py` - Redis/in-memory caching

**src/renderers/**
- `template_engine.py` - Jinja2 template processing
- `pdf_renderer.py` - PDF generation
- `excel_renderer.py` - Excel workbook creation
- `chart_builder.py` - Plotly/Matplotlib integration

**src/delivery/**
- `email.py` - SMTP email sender
- `webhook.py` - HTTP POST delivery
- `storage.py` - S3/local file storage

**src/api/**
- `server.py` - FastAPI/Flask server
- `routes.py` - API endpoints
- `schemas.py` - Pydantic models for validation

**src/cli/**
- `main.py` - Click-based CLI interface
- `commands.py` - CLI command implementations

**src/utils/**
- `logger.py` - Structured logging
- `exceptions.py` - Custom exception classes
- `helpers.py` - Common utility functions

## Dependencies & Rationale

### Core Dependencies
```python
# Data Processing
pandas>=2.0.0           # DataFrame operations, widely adopted
sqlalchemy>=2.0.0       # Database abstraction layer
pymongo>=4.5.0          # MongoDB driver
requests>=2.31.0        # HTTP client for APIs
pydantic>=2.5.0         # Data validation and settings

# Report Generation
jinja2>=3.1.0           # Template engine, de facto standard
weasyprint>=60.0        # HTML to PDF conversion
openpyxl>=3.1.0         # Excel file generation
plotly>=5.18.0          # Interactive charts
pillow>=10.1.0          # Image processing

# Web & API
fastapi>=0.105.0        # Modern async API framework
uvicorn>=0.25.0         # ASGI server
click>=8.1.0            # CLI framework

# Scheduling & Background Tasks
apscheduler>=3.10.0     # Advanced Python scheduler
celery>=5.3.0           # Distributed task queue (optional)
redis>=5.0.0            # Caching and task broker

# Testing & Quality
pytest>=7.4.0           # Testing framework
pytest-cov>=4.1.0       # Coverage reporting
black>=23.12.0          # Code formatter
ruff>=0.1.8             # Fast linter
mypy>=1.7.0             # Static type checker
```

### Dependency Rationale
- **Pandas:** Industry standard for data manipulation, excellent performance
- **SQLAlchemy:** Supports multiple databases with a single API
- **FastAPI:** Modern, fast, with automatic API documentation
- **Jinja2:** Battle-tested templating, used by Flask/Django
- **WeasyPrint:** Best Python library for HTML→PDF with CSS support
- **APScheduler:** Flexible scheduling without external dependencies
- **Pydantic:** Runtime type checking and validation

## Installation & Setup

### Prerequisites
```bash
# Python 3.10 or higher
python --version

# Optional: Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installation
```bash
# Clone the repository
git clone https://github.com/qvidal01/report-generator.git
cd report-generator

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e ".[dev]"

# Verify installation
report-generator --version
```

### Configuration
```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration with your credentials
nano config/config.yaml
```

### First Run
```bash
# Run a simple example report
report-generator generate examples/sales_report.yaml

# Start the web interface
report-generator serve --port 8080

# Schedule a recurring report
report-generator schedule examples/daily_metrics.yaml --cron "0 9 * * *"
```

## Programmatic Usage (API Surface)

### Python Library Usage
```python
from report_generator import ReportEngine, DataSource, Template

# Initialize engine
engine = ReportEngine(config_path="config.yaml")

# Define data sources
db_source = DataSource.from_database(
    "postgresql://user:pass@localhost/sales",
    query="SELECT * FROM orders WHERE date >= NOW() - INTERVAL '7 days'"
)

api_source = DataSource.from_api(
    "https://api.example.com/metrics",
    auth_token="your-token",
    method="GET"
)

# Load template
template = Template.from_file("templates/weekly_sales.html")

# Generate report
report = engine.generate(
    template=template,
    sources=[db_source, api_source],
    output_format="pdf",
    params={"title": "Weekly Sales Report"}
)

# Save or deliver
report.save("output/weekly_sales.pdf")
report.email(to="team@example.com", subject="Weekly Report")
```

### REST API Endpoints
```http
POST /api/v1/reports/generate
  - Body: { "template_id": "...", "sources": [...], "format": "pdf" }
  - Returns: { "report_id": "...", "status": "processing" }

GET /api/v1/reports/{report_id}
  - Returns: Report metadata and download URL

GET /api/v1/reports/{report_id}/download
  - Returns: Binary report file

POST /api/v1/schedules
  - Body: { "name": "...", "template_id": "...", "cron": "..." }
  - Returns: Schedule configuration

GET /api/v1/datasources
  - Returns: List of configured data sources

POST /api/v1/datasources/test
  - Body: Data source configuration
  - Returns: Connection test results
```

### CLI Commands
```bash
# Generate a report
report-generator generate <config-file> [--output <path>] [--format pdf|excel|html]

# List scheduled reports
report-generator schedule list

# Add a schedule
report-generator schedule add <config-file> --cron "0 9 * * *"

# Test data source connection
report-generator datasource test <source-config>

# Start API server
report-generator serve [--host 0.0.0.0] [--port 8080]

# Validate configuration
report-generator validate <config-file>
```

## MCP Server Assessment

### Is This a Good Fit for MCP?

**YES** - This project is an excellent candidate for an MCP (Model Context Protocol) server implementation.

### Rationale

1. **Tool-Based Architecture:** Report generation naturally maps to discrete tools/actions
2. **External Data Access:** MCP excels at providing structured access to external data sources
3. **Stateful Operations:** Report generation involves multi-step processes (fetch → transform → render → deliver)
4. **LLM Integration:** AI assistants could help users create reports through natural language

### MCP Server Capabilities

The Report Generator MCP server would expose these tools:

#### Tool 1: `generate_report`
```json
{
  "name": "generate_report",
  "description": "Generate a report from specified data sources and template",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template": {"type": "string", "description": "Template name or inline template"},
      "sources": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": {"enum": ["database", "api", "file"]},
            "config": {"type": "object"}
          }
        }
      },
      "output_format": {"enum": ["pdf", "excel", "html", "json"]},
      "parameters": {"type": "object", "description": "Template variables"}
    },
    "required": ["template", "sources", "output_format"]
  }
}
```

#### Tool 2: `query_datasource`
```json
{
  "name": "query_datasource",
  "description": "Execute a query against a configured data source",
  "inputSchema": {
    "type": "object",
    "properties": {
      "source_id": {"type": "string"},
      "query": {"type": "string"},
      "limit": {"type": "integer", "default": 100}
    },
    "required": ["source_id", "query"]
  }
}
```

#### Tool 3: `list_templates`
```json
{
  "name": "list_templates",
  "description": "List available report templates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "category": {"type": "string", "optional": true}
    }
  }
}
```

#### Tool 4: `schedule_report`
```json
{
  "name": "schedule_report",
  "description": "Schedule a recurring report generation",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template": {"type": "string"},
      "cron": {"type": "string", "description": "Cron expression"},
      "delivery": {
        "type": "object",
        "properties": {
          "method": {"enum": ["email", "webhook", "storage"]},
          "config": {"type": "object"}
        }
      }
    },
    "required": ["template", "cron"]
  }
}
```

### MCP Resources

The server would also expose report history and templates as resources:

```json
{
  "resources": [
    {
      "uri": "report-generator://reports/recent",
      "name": "Recent Reports",
      "description": "List of recently generated reports",
      "mimeType": "application/json"
    },
    {
      "uri": "report-generator://templates/{template_id}",
      "name": "Report Template",
      "description": "Access a specific report template",
      "mimeType": "text/html"
    },
    {
      "uri": "report-generator://schedules",
      "name": "Active Schedules",
      "description": "List of scheduled report jobs",
      "mimeType": "application/json"
    }
  ]
}
```

### Error Handling

The MCP server would implement robust error handling:
- **Authentication errors:** Invalid credentials for data sources
- **Validation errors:** Invalid template syntax or missing parameters
- **Data errors:** Failed queries or unreachable APIs
- **Generation errors:** Template rendering or PDF conversion failures

### Example MCP Interaction

```json
// User via LLM: "Generate a sales report for last week and email it to me"

// MCP Tool Call
{
  "name": "generate_report",
  "arguments": {
    "template": "weekly_sales",
    "sources": [
      {
        "type": "database",
        "config": {
          "connection": "sales_db",
          "query": "SELECT * FROM orders WHERE created_at >= NOW() - INTERVAL '7 days'"
        }
      }
    ],
    "output_format": "pdf",
    "parameters": {
      "title": "Weekly Sales Report",
      "date_range": "2025-11-12 to 2025-11-19"
    },
    "delivery": {
      "method": "email",
      "config": {
        "to": "user@example.com",
        "subject": "Weekly Sales Report"
      }
    }
  }
}

// MCP Response
{
  "content": [
    {
      "type": "text",
      "text": "Report generated successfully. PDF sent to user@example.com"
    },
    {
      "type": "resource",
      "resource": {
        "uri": "report-generator://reports/rpt_123abc",
        "mimeType": "application/pdf"
      }
    }
  ]
}
```

## Security Considerations

1. **Credential Management:**
   - Never store credentials in code
   - Support environment variables and secret management (AWS Secrets Manager, HashiCorp Vault)
   - Encrypt sensitive config files at rest

2. **Input Validation:**
   - Sanitize all SQL queries to prevent injection
   - Validate template syntax before rendering
   - Rate limiting on API endpoints

3. **Access Control:**
   - API key authentication for REST API
   - Role-based access for data sources
   - Audit logging for all report generation

4. **Data Privacy:**
   - Option to redact sensitive fields in reports
   - Secure deletion of temporary files
   - GDPR compliance for scheduled reports

## What I Learned (Topics & Resources)

This project demonstrates several important software engineering concepts:

### 1. **Data Pipeline Architecture**
- Building ETL (Extract, Transform, Load) systems
- Resource: *Data Pipelines Pocket Reference* by James Densmore

### 2. **Template Engines & Rendering**
- Server-side templating with Jinja2
- Resource: [Jinja2 Documentation](https://jinja.palletsprojects.com/)

### 3. **API Design Best Practices**
- RESTful API design with FastAPI
- Resource: [FastAPI Documentation](https://fastapi.tiangolo.com/)

### 4. **Scheduled Task Management**
- Cron expressions and background job processing
- Resource: [APScheduler User Guide](https://apscheduler.readthedocs.io/)

### 5. **PDF Generation in Python**
- HTML/CSS to PDF conversion
- Resource: [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)

### 6. **MCP (Model Context Protocol)**
- Building LLM-accessible tool servers
- Resource: [Anthropic MCP Documentation](https://modelcontextprotocol.io/)

### 7. **Testing Strategies**
- Unit testing with pytest, mocking external services
- Resource: *Python Testing with pytest* by Brian Okken

### 8. **Type Safety in Python**
- Using mypy and Pydantic for runtime/static checking
- Resource: [mypy documentation](https://mypy.readthedocs.io/)

## Future Enhancements

1. **Advanced Visualizations:** D3.js integration for interactive web reports
2. **Real-time Dashboards:** WebSocket support for live data updates
3. **AI-Powered Insights:** Integration with LLMs for automated analysis
4. **Multi-tenancy:** Support for multiple organizations with isolated data
5. **Report Builder UI:** Drag-and-drop interface for non-technical users
6. **Version Control:** Git-based template and configuration versioning
7. **Alerting:** Threshold-based alerts when metrics exceed limits
8. **Data Lineage:** Track data provenance through the pipeline

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Author:** AIQSO
**License:** MIT
