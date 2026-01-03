# MCP Server Guide

The Report Generator MCP (Model Context Protocol) server allows AI assistants like Claude to generate reports through natural language interactions.

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## What is MCP?

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external tools and data sources. The Report Generator MCP server exposes report generation capabilities that can be accessed by any MCP-compatible client.

### Benefits

- **Natural language interface**: Generate reports by describing what you want
- **AI-powered data analysis**: Let Claude help analyze and visualize your data
- **Automated workflows**: Chain together data fetching, transformation, and reporting
- **Safe execution**: All operations run in a controlled, sandboxed environment

## Installation

### Prerequisites

- Python 3.10 or higher
- Report Generator installed
- MCP Python SDK

### Install MCP Support

```bash
# Install Report Generator with MCP support
pip install "report-generator[mcp]"

# Or if installing from source
pip install -e ".[mcp]"
```

### Verify Installation

```bash
# Test that MCP server can start
python -m mcp_server.server --help
```

## Configuration

### Claude Desktop

To use the MCP server with Claude Desktop, add the configuration to your Claude Desktop config file:

**Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "report-generator": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "DATABASE_URL": "postgresql://user:password@localhost/reports",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "your-email@example.com",
        "SMTP_PASSWORD": "your-app-password",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Environment Variables

The MCP server respects all Report Generator environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | No |
| `REDIS_URL` | Redis connection for caching | No |
| `SMTP_HOST` | SMTP server for email delivery | No |
| `SMTP_USERNAME` | SMTP authentication username | No |
| `SMTP_PASSWORD` | SMTP authentication password | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING) | No |

### Security Considerations

- **Credentials**: Store sensitive credentials in environment variables, not in code
- **File Access**: The MCP server can access files within its working directory
- **Network Access**: The server can make outbound network requests to APIs and databases
- **Sandboxing**: Templates are rendered in a Jinja2 sandbox to prevent code execution

## Available Tools

### 1. `generate_report`

Generate a report from data sources and a template.

**Parameters:**
- `template` (string): Template path or inline HTML
- `sources` (array): List of data source configurations
- `output_format` (string): Output format - "pdf", "excel", "html", or "json"
- `parameters` (object, optional): Template variables

**Example:**

```json
{
  "template": "templates/sales_report.html",
  "sources": [
    {
      "type": "database",
      "connection_string": "postgresql://localhost/sales",
      "query": "SELECT * FROM orders WHERE date >= '2025-11-01'",
      "name": "sales_data"
    }
  ],
  "output_format": "pdf",
  "parameters": {
    "title": "November Sales Report",
    "date": "2025-11-19"
  }
}
```

### 2. `list_templates`

List available report templates.

**Parameters:**
- `category` (string, optional): Filter by category

**Example:**

```json
{
  "category": "sales"
}
```

### 3. `test_datasource`

Test connectivity to a data source.

**Parameters:**
- `source_config` (object): Data source configuration

**Example:**

```json
{
  "type": "database",
  "connection_string": "postgresql://localhost/sales"
}
```

## Usage Examples

### Example 1: Generate Sales Report

**User prompt to Claude:**
> "Generate a PDF sales report from the database showing all orders from last week."

**Claude calls `generate_report` tool:**

```json
{
  "template": "<html><body><h1>{{ title }}</h1><table>{% for order in data %}...</table></body></html>",
  "sources": [
    {
      "type": "database",
      "connection_string": "postgresql://localhost/sales",
      "query": "SELECT * FROM orders WHERE date >= CURRENT_DATE - INTERVAL '7 days'",
      "name": "orders"
    }
  ],
  "output_format": "pdf",
  "parameters": {
    "title": "Weekly Sales Report"
  }
}
```

### Example 2: API Data Report

**User prompt:**
> "Create a report from our Stripe API showing revenue for November."

**Claude calls `generate_report` tool:**

```json
{
  "template": "templates/revenue_report.html",
  "sources": [
    {
      "type": "api",
      "url": "https://api.stripe.com/v1/charges",
      "auth_token": "sk_test_...",
      "name": "stripe_charges"
    }
  ],
  "output_format": "pdf"
}
```

### Example 3: Multi-Source Report

**User prompt:**
> "Combine data from our database and API to create a comprehensive metrics dashboard."

**Claude calls `generate_report` tool:**

```json
{
  "template": "templates/dashboard.html",
  "sources": [
    {
      "type": "database",
      "connection_string": "postgresql://localhost/analytics",
      "query": "SELECT * FROM metrics WHERE date = CURRENT_DATE",
      "name": "db_metrics"
    },
    {
      "type": "api",
      "url": "https://api.example.com/external_metrics",
      "auth_token": "your-token",
      "name": "api_metrics"
    }
  ],
  "output_format": "html"
}
```

## Troubleshooting

### MCP Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
pip install "report-generator[mcp]"
```

### Database Connection Fails

**Error:** `DataSourceError: Failed to connect to database`

**Solutions:**
1. Verify `DATABASE_URL` is set correctly in config
2. Check database server is running
3. Verify credentials and network access
4. Test connection manually:
   ```python
   from sqlalchemy import create_engine
   engine = create_engine("your-connection-string")
   engine.connect()
   ```

### Template Rendering Fails

**Error:** `TemplateError: Failed to parse template`

**Solutions:**
1. Check Jinja2 syntax in template
2. Verify all template variables are provided in `parameters`
3. Test template locally:
   ```python
   from report_generator.renderers import Template
   template = Template.from_file("your-template.html")
   template.render({"title": "Test"})
   ```

### PDF Generation Fails

**Error:** `RenderError: Failed to generate PDF`

**Solutions:**
1. Install WeasyPrint dependencies:
   - macOS: `brew install pango`
   - Ubuntu: `sudo apt-get install libpango-1.0-0`
   - Windows: Install GTK+ runtime
2. Verify WeasyPrint is installed: `pip show weasyprint`
3. Test PDF generation:
   ```python
   from weasyprint import HTML
   HTML(string="<h1>Test</h1>").write_pdf("test.pdf")
   ```

### Permission Denied Errors

**Error:** `PermissionError: [Errno 13] Permission denied: 'output/report.pdf'`

**Solutions:**
1. Verify `output/` directory exists and is writable
2. Check file permissions: `chmod 755 output/`
3. Run with appropriate user permissions

## Advanced Configuration

### Custom Output Directory

Set output directory via environment variable:

```json
{
  "env": {
    "REPORT_OUTPUT_DIR": "/path/to/custom/output"
  }
}
```

### Logging

Enable debug logging for troubleshooting:

```json
{
  "env": {
    "LOG_LEVEL": "DEBUG"
  }
}
```

Logs will include:
- Data source connection attempts
- Query execution
- Template rendering steps
- PDF generation progress

### Performance Tuning

For large reports, adjust timeout and cache settings:

```python
# In your template or config
config = {
    "timeout": 60,  # Seconds
    "cache_ttl": 300,  # 5 minutes
}
```

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Report Generator Documentation](../README.md)
- [API Reference](API_REFERENCE.md)
- [GitHub Issues](https://github.com/qvidal01/report-generator/issues)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review logs with `LOG_LEVEL=DEBUG`
3. Search [existing issues](https://github.com/qvidal01/report-generator/issues)
4. Open a new issue with:
   - MCP server logs
   - Configuration (redact credentials)
   - Steps to reproduce
   - Expected vs actual behavior

---

**Happy Reporting!** 📊
