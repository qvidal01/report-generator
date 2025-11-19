# Contributing to Report Generator

First off, thank you for considering contributing to Report Generator! It's people like you that make this project better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Good First Issues](#good-first-issues)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, config files)
- **Describe the behavior you observed** and what you expected
- **Include logs and error messages**
- **Specify your environment** (OS, Python version, package versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most users
- **List any similar features** in other tools if applicable

### Your First Code Contribution

Unsure where to begin? Look for issues tagged with:
- `good first issue` - Issues good for newcomers
- `help wanted` - Issues where we'd appreciate community help
- `documentation` - Improvements to docs

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- (Optional) Redis for caching features
- (Optional) PostgreSQL/MySQL for database testing

### Setup Steps

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/report-generator.git
cd report-generator

# 3. Add upstream remote
git remote add upstream https://github.com/qvidal01/report-generator.git

# 4. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install development dependencies
pip install -e ".[dev]"

# 6. Install pre-commit hooks
pre-commit install

# 7. Copy environment template
cp .env.example .env
# Edit .env with your test credentials

# 8. Run tests to verify setup
pytest
```

### Project Structure

```
report-generator/
├── src/report_generator/    # Main source code
│   ├── core/                 # Core engine and orchestration
│   ├── datasources/          # Data source connectors
│   ├── processors/           # Data transformation
│   ├── renderers/            # Report rendering (PDF, Excel)
│   ├── delivery/             # Delivery mechanisms
│   ├── api/                  # REST API
│   ├── cli/                  # Command-line interface
│   └── utils/                # Utilities and helpers
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
├── docs/                     # Documentation
├── examples/                 # Usage examples
└── config/                   # Configuration examples
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Add tests** for your changes:
   - Unit tests for new functions/classes
   - Integration tests for new features
   - Aim for >80% coverage

4. **Update documentation**:
   - Add docstrings to new functions/classes
   - Update README.md if adding user-facing features
   - Update relevant docs in `docs/`

5. **Run the test suite**:
   ```bash
   # Format code
   black .

   # Lint code
   ruff check .

   # Type check
   mypy src/report_generator

   # Run tests
   pytest --cov=report_generator

   # Run all checks
   pytest && black . && ruff check . && mypy src/
   ```

6. **Commit your changes**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/) format
   - Examples:
     - `feat: add MongoDB data source connector`
     - `fix: handle missing template variables gracefully`
     - `docs: update API reference for new endpoints`
     - `test: add integration tests for email delivery`

### Submitting

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Reference related issues (`Fixes #123`, `Closes #456`)
   - Describe what changes you made and why
   - Include screenshots for UI changes
   - Mark as draft if not ready for review

3. **Respond to feedback**:
   - Address review comments promptly
   - Push additional commits to the same branch
   - Request re-review when ready

### PR Requirements

- ✅ All CI checks must pass
- ✅ Code coverage must not decrease
- ✅ At least one approving review from a maintainer
- ✅ Branch must be up to date with `main`
- ✅ Commit messages follow conventional format

## Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (configured in pyproject.toml)
- **Formatter**: Black (automated)
- **Linter**: Ruff (catches common issues)
- **Type hints**: Required for all function signatures

### Code Quality

```python
# ✅ GOOD
def fetch_data(source: DataSource, limit: int = 100) -> pd.DataFrame:
    """
    Fetch data from a data source.

    Args:
        source: Data source to fetch from
        limit: Maximum number of rows to fetch

    Returns:
        DataFrame with fetched data

    Raises:
        DataSourceError: If fetch fails
    """
    logger.info("fetching_data", source=source.name, limit=limit)
    try:
        df = source.fetch()
        return df.head(limit)
    except Exception as e:
        logger.error("fetch_failed", source=source.name, error=str(e))
        raise DataSourceError(f"Failed to fetch from {source.name}: {e}")

# ❌ BAD
def fetch_data(source, limit=100):  # No type hints
    # No docstring
    df = source.fetch()  # No error handling
    return df.head(limit)
```

### Naming Conventions

- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`

### Docstrings

Use Google-style docstrings:

```python
def complex_function(arg1: str, arg2: int, arg3: bool = False) -> dict[str, Any]:
    """
    Short one-line summary.

    Longer description if needed. Can span multiple
    lines and include implementation details.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        arg3: Description of optional arg3 (default: False)

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
        TypeError: When arg types are wrong

    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        {'status': 'ok'}
    """
    pass
```

### Error Handling

- Use custom exception classes from `utils.exceptions`
- Log errors with structured logging
- Provide helpful error messages
- Don't swallow exceptions silently

```python
# ✅ GOOD
try:
    result = dangerous_operation()
except SpecificError as e:
    logger.error("operation_failed", error=str(e))
    raise DataSourceError(f"Operation failed: {e}")

# ❌ BAD
try:
    result = dangerous_operation()
except:  # Too broad, silent failure
    pass
```

## Testing Guidelines

### Writing Tests

- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test interactions between components
- **Use fixtures**: Define reusable test data in `conftest.py`
- **Test edge cases**: Empty inputs, invalid data, network errors
- **Use descriptive names**: Test names should describe what they test

### Test Structure

```python
# tests/unit/test_datasources.py
import pytest
from report_generator.datasources import DatabaseSource
from report_generator.utils.exceptions import DataSourceError

class TestDatabaseSource:
    """Tests for DatabaseSource class."""

    def test_valid_connection(self, mock_db_engine):
        """Test successful database connection."""
        source = DatabaseSource(
            name="test",
            connection_string="sqlite:///:memory:",
            query="SELECT 1"
        )
        assert source.test_connection() is True

    def test_invalid_query_raises_error(self):
        """Test that invalid SQL query raises DataSourceError."""
        source = DatabaseSource(
            name="test",
            connection_string="sqlite:///:memory:",
            query="INVALID SQL"
        )
        with pytest.raises(DataSourceError):
            source.fetch()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_datasources.py

# Run specific test
pytest tests/unit/test_datasources.py::TestDatabaseSource::test_valid_connection

# Run with coverage
pytest --cov=report_generator --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests matching pattern
pytest -k "database"
```

## Documentation

### Types of Documentation

1. **Code documentation** (docstrings):
   - Required for all public APIs
   - Use Google-style format

2. **User documentation** (docs/):
   - Getting started guides
   - API reference
   - Usage examples

3. **Examples** (examples/):
   - Runnable code samples
   - Cover common use cases

### Updating Documentation

- Update docs in the same PR as code changes
- Run examples to verify they work
- Keep documentation concise and practical
- Include screenshots/diagrams when helpful

## Good First Issues

Looking for a place to start? Here are some ideas:

### Easy (< 2 hours)
- Add a new data source connector (e.g., Google Sheets API)
- Improve error messages to be more helpful
- Add more example templates
- Fix typos in documentation
- Add unit tests for untested functions

### Medium (2-8 hours)
- Add a new export format (e.g., CSV, Markdown)
- Implement email delivery with attachments
- Add data validation rules for common cases
- Write a comprehensive tutorial
- Add Dockerfile for containerization

### Hard (> 8 hours)
- Implement async data fetching for performance
- Add real-time dashboard with WebSockets
- Integrate with cloud storage (S3, GCS)
- Build visual report builder UI
- Add AI-powered data insights

## Questions?

- **General questions**: Open a [GitHub Discussion](https://github.com/qvidal01/report-generator/discussions)
- **Bug reports**: Open a [GitHub Issue](https://github.com/qvidal01/report-generator/issues)
- **Security issues**: Email contact@aiqso.io (do not open public issue)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
