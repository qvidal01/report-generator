#!/usr/bin/env python
"""
Basic Report Example

This example demonstrates how to generate a simple report from a CSV file.

Requirements:
- Sample data file (creates one if not exists)

Usage:
    python examples/basic_report.py
"""

from pathlib import Path

import pandas as pd

from report_generator import DataSource, ReportEngine, Template


def create_sample_data():
    """Create sample CSV data if it doesn't exist."""
    data_file = Path("examples/data/sales.csv")
    data_file.parent.mkdir(parents=True, exist_ok=True)

    if not data_file.exists():
        df = pd.DataFrame({
            "product": ["Widget A", "Widget B", "Widget C", "Widget D", "Widget E"],
            "sales": [150, 230, 180, 295, 210],
            "revenue": [1500.00, 2300.00, 1800.00, 2950.00, 2100.00],
            "region": ["North", "South", "East", "West", "North"],
        })
        df.to_csv(data_file, index=False)
        print(f"✅ Created sample data: {data_file}")

    return str(data_file)


def main():
    """Generate a basic report from CSV data."""
    print("=" * 60)
    print("Basic Report Example")
    print("=" * 60)

    # Step 1: Create sample data
    print("\n1. Creating sample data...")
    data_file = create_sample_data()

    # Step 2: Define data source
    print("\n2. Configuring data source...")
    source = DataSource.from_file(data_file)

    # Step 3: Create simple template
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
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }
            th {
                background-color: #4CAF50;
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
            .footer {
                margin-top: 30px;
                padding-top: 10px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <p>Generated on: {{ date }}</p>

        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Sales</th>
                    <th>Revenue</th>
                    <th>Region</th>
                </tr>
            </thead>
            <tbody>
                {% for index, row in data.iterrows() %}
                <tr>
                    <td>{{ row['product'] }}</td>
                    <td>{{ row['sales'] }}</td>
                    <td>${{ "%.2f"|format(row['revenue']) }}</td>
                    <td>{{ row['region'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            <p>Total Sales: {{ data['sales'].sum() }}</p>
            <p>Total Revenue: ${{ "%.2f"|format(data['revenue'].sum()) }}</p>
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
        sources=[source],
        output_format="html",  # Use HTML for quick preview
        params={
            "title": "Sales Report",
            "date": "2025-11-19"
        }
    )

    # Step 5: Save report
    output_path = "output/basic_report.html"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    report.save(output_path)

    print("\n✅ Report generated successfully!")
    print(f"📄 Saved to: {output_path}")
    print(f"📊 Size: {len(report.content)} bytes")
    print(f"\n💡 Open {output_path} in your browser to view the report")

    # Optional: Generate PDF version
    try:
        print("\n5. Generating PDF version...")
        pdf_report = engine.generate(
            template=template,
            sources=[source],
            output_format="pdf",
            params={
                "title": "Sales Report",
                "date": "2025-11-19"
            }
        )
        pdf_output = "output/basic_report.pdf"
        pdf_report.save(pdf_output)
        print(f"✅ PDF saved to: {pdf_output}")
    except ImportError:
        print("⚠️  WeasyPrint not installed. Skipping PDF generation.")
        print("   Install with: pip install weasyprint")


if __name__ == "__main__":
    main()
