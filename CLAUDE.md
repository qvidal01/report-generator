# Report Generator - Claude Reference

## Quick Overview
Multi-source report generation system. Connects to databases, APIs, and files to generate PDF/Excel/HTML reports with scheduling and delivery.

## Tech Stack
- **Framework:** FastAPI + Uvicorn
- **Language:** Python 3.10+
- **Data:** Pandas
- **Database:** SQLAlchemy, PyMongo
- **Templates:** Jinja2
- **PDF:** WeasyPrint
- **Charts:** Plotly
- **Excel:** OpenPyXL
- **Scheduling:** APScheduler
- **Cache:** Redis
- **AI:** MCP Server

## Project Structure
```
src/report_generator/
├── datasources/         # Data source connectors
├── processors/          # Data processing engines
├── renderers/           # Output (PDF, Excel, HTML)
├── templates/           # Jinja2 report templates
├── scheduling/          # APScheduler integration
├── storage/             # Storage backends
├── api/                 # FastAPI endpoints
├── cli/                 # Command-line interface
├── mcp_server/          # MCP server for Claude
└── models/              # Data models

tests/                   # Unit & integration tests
docs/                    # API reference
examples/                # Usage examples
docker-compose.yml       # Redis, PostgreSQL
```

## Quick Commands
```bash
# Install
pip install -e ".[dev]"

# Run API
uvicorn src.report_generator.api:app --reload

# Generate report via CLI
python -m report_generator generate --template sales --format pdf

# Docker
docker-compose up -d
```

## Data Sources
- **Databases:** PostgreSQL, MySQL, MongoDB
- **APIs:** Any REST API with auth
- **Files:** CSV, Excel, JSON
- **Cloud:** S3, GCS (planned)

## Output Formats
- PDF (WeasyPrint)
- Excel (OpenPyXL)
- HTML

## Key Features
- Multi-source connectivity
- Customizable Jinja2 templates
- Automated scheduling (cron)
- Smart delivery (Email, webhook, S3)
- Rich visualizations (Plotly)
- REST API with OpenAPI docs
- Async processing & caching
- MCP Server for Claude

## Use Cases
- Sales reports (daily/weekly/monthly)
- Financial summaries
- Analytics dashboards
- Compliance reports
- Performance metrics

## Status: Beta (v1.0)
- All major features implemented
- MCP server complete
- Full documentation

## Documentation
- `ANALYSIS_SUMMARY.md` - Architecture
- `ISSUES_FOUND.md` - Known issues
- `IMPROVEMENT_PLAN.md` - Roadmap
