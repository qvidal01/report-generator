#!/usr/bin/env python
"""
Multi-Source Report Example

This example demonstrates combining data from multiple sources:
- CSV file (local sales data)
- Mock API (external metrics)

Requirements:
- Sample data files

Usage:
    python examples/multi_source_report.py
"""

import json
from pathlib import Path

import pandas as pd

from report_generator import DataSource, ReportEngine, Template


def create_sample_data():
    """Create sample data files."""
    # Create sales CSV
    sales_file = Path("examples/data/sales.csv")
    sales_file.parent.mkdir(parents=True, exist_ok=True)

    df_sales = pd.DataFrame({
        "product": ["Widget A", "Widget B", "Widget C"],
        "units_sold": [150, 230, 180],
        "revenue": [1500.00, 2300.00, 1800.00],
    })
    df_sales.to_csv(sales_file, index=False)

    # Create metrics JSON (simulating API response)
    metrics_file = Path("examples/data/metrics.json")
    metrics_data = [
        {"metric": "Active Users", "value": 1250, "change": "+15%"},
        {"metric": "Conversion Rate", "value": 3.2, "change": "+0.5%"},
        {"metric": "Avg Order Value", "value": 87.50, "change": "-2.1%"},
    ]

    with open(metrics_file, "w") as f:
        json.dump(metrics_data, f, indent=2)

    print("✅ Created sample data files")
    return str(sales_file), str(metrics_file)


def main():
    """Generate report combining multiple data sources."""
    print("=" * 60)
    print("Multi-Source Report Example")
    print("=" * 60)

    # Step 1: Create sample data
    print("\n1. Creating sample data...")
    sales_file, metrics_file = create_sample_data()

    # Step 2: Define data sources
    print("\n2. Configuring data sources...")
    sales_source = DataSource.from_file(sales_file, name="sales")
    metrics_source = DataSource.from_file(metrics_file, name="metrics")

    # Step 3: Create template
    print("\n3. Creating template...")
    template_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ title }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 5px;
            }
            h2 {
                color: #34495e;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 20px 0;
            }
            .metric-card {
                background: #ecf0f1;
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }
            .metric-label {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 8px;
            }
            .metric-value {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
            }
            .metric-change {
                font-size: 14px;
                margin-top: 8px;
            }
            .positive { color: #27ae60; }
            .negative { color: #e74c3c; }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }
            th {
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
            }
            td {
                border: 1px solid #ddd;
                padding: 10px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{{ title }}</h1>
            <p style="color: #7f8c8d;">{{ date }}</p>

            <h2>📊 Key Metrics</h2>
            <div class="metrics-grid">
                {% for metric in data.metrics.to_dict('records') %}
                <div class="metric-card">
                    <div class="metric-label">{{ metric.metric }}</div>
                    <div class="metric-value">{{ metric.value }}</div>
                    <div class="metric-change {{ 'positive' if '+' in metric.change else 'negative' }}">
                        {{ metric.change }}
                    </div>
                </div>
                {% endfor %}
            </div>

            <h2>💰 Sales Performance</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Units Sold</th>
                        <th>Revenue</th>
                        <th>Avg Price</th>
                    </tr>
                </thead>
                <tbody>
                    {% for index, row in data.sales.iterrows() %}
                    <tr>
                        <td>{{ row['product'] }}</td>
                        <td>{{ row['units_sold'] }}</td>
                        <td>${{ "%.2f"|format(row['revenue']) }}</td>
                        <td>${{ "%.2f"|format(row['revenue'] / row['units_sold']) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <div style="margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 6px;">
                <h3 style="margin-top: 0;">Summary</h3>
                <p><strong>Total Units:</strong> {{ data.sales['units_sold'].sum() }}</p>
                <p><strong>Total Revenue:</strong> ${{ "%.2f"|format(data.sales['revenue'].sum()) }}</p>
                <p><strong>Data Sources:</strong> Sales Database, Analytics API</p>
            </div>
        </div>
    </body>
    </html>
    """

    template = Template.from_string(template_html)

    # Step 4: Generate report
    print("\n4. Generating report...")
    engine = ReportEngine()

    report = engine.generate(
        template=template,
        sources=[sales_source, metrics_source],
        output_format="html",
        params={
            "title": "Monthly Performance Report",
            "date": "November 2025"
        }
    )

    # Step 5: Save report
    output_path = "output/multi_source_report.html"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    report.save(output_path)

    print("\n✅ Multi-source report generated successfully!")
    print(f"📄 Saved to: {output_path}")
    print(f"📊 Combined data from {len([sales_source, metrics_source])} sources")
    print("\n💡 This example demonstrates:")
    print("   - Combining data from multiple sources (CSV + JSON)")
    print("   - Creating a dashboard-style layout")
    print("   - Using conditional formatting in templates")


if __name__ == "__main__":
    main()
