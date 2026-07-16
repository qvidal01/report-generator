---
runbook: true
repo: report-generator
status: paused
type: tool
updated: 2026-07-16
health: unknown
deploy: GitHub Pages docs deploy via .github/workflows/docs.yml using mkdocs build and actions/deploy-pages
next: implement source code and tests from IMPROVEMENT_PLAN.md
---

# report-generator — Runbook

## Purpose

Multi-source data aggregation and report generation tool. The README describes a Python tool for pulling data from databases, REST APIs, and files, then generating reports in PDF, Excel, HTML, and JSON formats. Documented use cases include sales reports, financial summaries, analytics dashboards, compliance reports, and performance metrics.

## Stack

Python 3.10+ tool packaged with setuptools. Core stack from repo config/docs: FastAPI, Uvicorn, Click, Pandas, SQLAlchemy, PyMongo, requests/httpx, Pydantic, Jinja2, WeasyPrint, OpenPyXL, Plotly, Pillow, APScheduler, Redis, python-dotenv, PyYAML, structlog, MkDocs Material. Optional extras: MCP, Celery, monitoring.

## Where it runs

Known from repo docs/config:

- Local Python environment via editable install
- Local REST API server via `report-generator serve` or `uvicorn`
- MCP server via `python -m mcp_server.server`
- Documentation site through GitHub Pages workflow and `mkdocs.yml`
- Docker is described in README/CLAUDE.md, but Dockerfile/docker-compose files were not verified in the allowed repo materials

Unknown: production application host, live API base URL, database/Redis/SMTP hosts.

## Run / deploy

Install for development:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Run tests and checks:

```bash
pytest
black --check .
ruff check .
mypy src/
```

Run the API:

```bash
report-generator serve --host 0.0.0.0 --port 8080
```

Alternate API command from CLAUDE.md:

```bash
uvicorn src.report_generator.api:app --reload
```

Generate a report:

```bash
report-generator generate examples/sales_report.yaml
```

Run the MCP server:

```bash
python -m mcp_server.server --help
```

Build docs locally:

```bash
mkdocs build
```

Deploy docs:

```bash
git push origin main
```

Docs deploy through GitHub Pages when docs, `mkdocs.yml`, or the docs workflow change on `main` or `master`.

## Health & recovery

Known health endpoint from README:

```bash
curl http://localhost:8080/health
```

Recovery is unknown. For local failures, verify dependencies, environment variables, and service prerequisites from README and docs/MCP_SERVER.md. Optional services include Redis and database backends. MCP troubleshooting notes cover missing MCP dependency and database connection failures.

## Current status

Git recency indicates paused: the most recent commit is `19f9733` on 2026-01-28, which is less than 180 days but more than 30 days before 2026-07-16. The latest 30 commits are all recent setup/documentation work: docs deployment workflow, API reference, getting started guide, docs homepage, MkDocs config, AI code quality workflow, and ruff auto-fixes. CLAUDE.md and package metadata describe Beta v1.0, while older planning docs still list implementation code and tests as required work.

## Links

- README: `README.md`
- Claude reference: `CLAUDE.md`
- Docs home: `docs/index.md`
- Getting started: `docs/getting-started.md`
- API reference: `docs/API_REFERENCE.md`
- MCP guide: `docs/MCP_SERVER.md`
- MkDocs config: `mkdocs.yml`
- GitHub repository: `https://github.com/qvidal01/report-generator`
- Configured docs site: `https://qvidal01.github.io/report-generator/`
- Odoo project: unknown
