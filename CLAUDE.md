# Report Generator - Claude Reference

## Quick Overview
Multi-source report generation system. Connects to databases, APIs, and files to generate PDF/Excel/HTML/JSON reports via Python library, CLI, or MCP server. Scheduling, delivery, and REST API are planned but not yet implemented.

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
├── core/                # Report engine (generate, save)
├── datasources/         # Data source connectors (database, API, file)
├── renderers/           # Output rendering (PDF/Excel/HTML/JSON, Jinja2)
├── cli/                 # Command-line interface (generate; serve is a stub)
├── utils/               # Config, logging, validators, helpers
├── api/                 # 🚧 Stub — FastAPI endpoints planned
├── delivery/            # 🚧 Stub — email/webhook/S3 planned
└── processors/          # 🚧 Stub — data processing engines planned

mcp_server/              # MCP server for Claude (repo root, not src/)
tests/                   # Unit tests (65 tests, ~84% coverage)
docs/                    # API reference, runbook, MCP docs
examples/                # basic_report.py, multi_source_report.py
```
No Dockerfile or docker-compose.yml yet (planned).

## Quick Commands
```bash
# Install
pip install -e ".[dev]"

# Generate report via CLI
report-generator generate config/report.yaml --output report.pdf --format pdf

# Run tests (also: black --check ., ruff check ., mypy src/report_generator)
pytest
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
- JSON

## Key Features
**Implemented:**
- Multi-source connectivity (PostgreSQL, MySQL, MongoDB, REST APIs, CSV/Excel/JSON)
- Customizable Jinja2 templates (sandboxed)
- Rich visualizations (Plotly)
- MCP Server for Claude

**Planned (🚧 stubs or absent):**
- Automated scheduling (cron) — APScheduler is a dependency but unused
- Smart delivery (email, webhook, S3) — methods raise NotImplementedError
- REST API with OpenAPI docs — `api/` is empty, `serve` command is a stub
- Async processing & Redis caching

## Use Cases
- Sales reports (daily/weekly/monthly)
- Financial summaries
- Analytics dashboards
- Compliance reports
- Performance metrics

## Status: Beta (v1.0) — updated 2026-07-16
- Core pipeline (datasources → engine → renderers), CLI generate, and MCP server work
- REST API, scheduling, and delivery are NOT implemented (see Key Features)
- CI green (pytest 9, black 26 pinned, ruff, mypy); pip-audit clean

## Documentation
- `ANALYSIS_SUMMARY.md` - Architecture
- `ISSUES_FOUND.md` - Historical pre-implementation analysis (2025-11)
- `IMPROVEMENT_PLAN.md` - Roadmap
- `docs/RUNBOOK.md` - Fleet runbook
