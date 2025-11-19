# Report Generator Examples

This directory contains runnable examples demonstrating various features of Report Generator.

## Examples Overview

### 1. [basic_report.py](basic_report.py)
**Difficulty:** Beginner
**Duration:** 2 minutes

Demonstrates:
- Loading data from a CSV file
- Creating a simple HTML template
- Generating HTML and PDF reports
- Saving reports to disk

**Run:**
```bash
python examples/basic_report.py
```

### 2. [multi_source_report.py](multi_source_report.py)
**Difficulty:** Intermediate
**Duration:** 3 minutes

Demonstrates:
- Combining data from multiple sources (CSV + JSON)
- Creating dashboard-style layouts
- Using Jinja2 template features (loops, conditionals)
- Grid layouts with CSS

**Run:**
```bash
python examples/multi_source_report.py
```

### 3. [custom_template.py](custom_template.py)
**Difficulty:** Intermediate
**Duration:** 5 minutes

Demonstrates:
- Loading templates from files
- Adding charts with Plotly (if installed)
- Custom CSS styling
- Template variables and parameters

**Run:**
```bash
# Install optional charting dependency
pip install plotly kaleido

python examples/custom_template.py
```

### 4. [database_report.py](database_report.py)
**Difficulty:** Advanced
**Duration:** 5 minutes

**Prerequisites:**
- SQLite (included with Python)
- Or PostgreSQL/MySQL server

Demonstrates:
- Connecting to SQL databases
- Executing queries with SQLAlchemy
- Parameterized queries for security
- Error handling

**Run:**
```bash
python examples/database_report.py
```

### 5. [api_report.py](api_report.py)
**Difficulty:** Advanced
**Duration:** 5 minutes

Demonstrates:
- Fetching data from REST APIs
- Authentication with API keys
- Handling JSON responses
- Retry logic for reliability

**Run:**
```bash
python examples/api_report.py
```

## Directory Structure

```
examples/
├── README.md                    # This file
├── basic_report.py              # Simple CSV → Report
├── multi_source_report.py       # Multiple data sources
├── custom_template.py           # Custom templates & charts
├── database_report.py           # Database integration
├── api_report.py                # API integration
├── data/                        # Sample data files
│   ├── sales.csv
│   ├── metrics.json
│   └── ...
└── templates/                   # Example templates
    ├── simple.html
    ├── dashboard.html
    └── ...
```

## Common Tasks

### Generate a Simple Report
```bash
python examples/basic_report.py
```

### View Generated Reports
```bash
# HTML reports - open in browser
open output/basic_report.html

# PDF reports - open with PDF viewer
open output/basic_report.pdf
```

### Modify Examples

All examples are self-contained Python scripts. You can:

1. **Edit the template:**
   ```python
   template_html = """
   <html>
       <h1>{{ title }}</h1>
       <!-- Your custom HTML -->
   </html>
   """
   ```

2. **Change the data source:**
   ```python
   source = DataSource.from_file("your_data.csv")
   ```

3. **Customize parameters:**
   ```python
   params = {
       "title": "Your Custom Title",
       "company": "Your Company",
       "date": datetime.now().strftime("%Y-%m-%d")
   }
   ```

## Tips & Best Practices

### 1. Data Sources

**CSV Files:**
```python
source = DataSource.from_file("data/sales.csv")
```

**Databases:**
```python
source = DataSource.from_database(
    connection_string="postgresql://user:pass@localhost/db",
    query="SELECT * FROM sales WHERE date >= CURRENT_DATE - 7"
)
```

**APIs:**
```python
source = DataSource.from_api(
    url="https://api.example.com/data",
    auth_token="your-token"
)
```

### 2. Templates

**Keep templates simple:**
- Use semantic HTML
- Add CSS for styling
- Avoid complex logic in templates

**Template variables:**
```python
params = {
    "title": "My Report",
    "date": "2025-11-19",
    "author": "John Doe"
}
```

**Accessing data in templates:**
```html
<!-- Iterate over DataFrame rows -->
{% for index, row in data.iterrows() %}
    <tr>
        <td>{{ row['column_name'] }}</td>
    </tr>
{% endfor %}

<!-- Access DataFrame methods -->
<p>Total: {{ data['sales'].sum() }}</p>
<p>Average: {{ data['sales'].mean() }}</p>
```

### 3. Output Formats

**HTML** - Fast, good for preview:
```python
output_format="html"
```

**PDF** - Professional documents:
```python
output_format="pdf"  # Requires weasyprint
```

**JSON** - Data export:
```python
output_format="json"
```

**Excel** - Spreadsheet format (coming soon):
```python
output_format="excel"  # Requires openpyxl
```

### 4. Error Handling

Always wrap report generation in try/except:

```python
try:
    report = engine.generate(template, sources, "pdf")
    report.save("output/report.pdf")
except DataSourceError as e:
    print(f"Data source error: {e}")
except TemplateError as e:
    print(f"Template error: {e}")
except RenderError as e:
    print(f"Rendering error: {e}")
```

## Troubleshooting

### Import Error: No module named 'report_generator'

**Solution:**
```bash
# Install from source
pip install -e .

# Or install from PyPI
pip install report-generator
```

### WeasyPrint PDF Generation Fails

**Solution:**
```bash
# macOS
brew install pango

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# Windows
# Download and install GTK+ runtime
```

### Data File Not Found

**Solution:**
Most examples create sample data automatically. If you see this error:
1. Run the example once to generate data
2. Check the `examples/data/` directory
3. Verify file paths in the script

## Next Steps

1. **Modify examples** to use your own data
2. **Create custom templates** for your reports
3. **Integrate with your database** or APIs
4. **Schedule reports** with cron or similar tools
5. **Deploy as a service** with the REST API

## Additional Resources

- [Main Documentation](../README.md)
- [API Reference](../docs/API_REFERENCE.md)
- [MCP Server Guide](../docs/MCP_SERVER.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Questions?

- Open an [issue](https://github.com/qvidal01/report-generator/issues)
- Start a [discussion](https://github.com/qvidal01/report-generator/discussions)
- Check the [FAQ](../docs/FAQ.md)

---

Happy reporting! 📊
