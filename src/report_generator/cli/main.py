"""CLI entry point for report-generator command."""

import click

from report_generator import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Report Generator CLI - Multi-source data aggregation and report generation."""
    pass


@cli.command()
@click.argument("config_file")
@click.option("--output", "-o", help="Output file path")
@click.option("--format", "-f", default="pdf", help="Output format (pdf, excel, html, json)")
def generate(config_file: str, output: str | None, format: str) -> None:
    """Generate a report from configuration file."""
    click.echo(f"Generating report from {config_file}...")
    click.echo("Note: Full implementation coming soon!")
    # TODO: Implement report generation


@cli.command()
@click.option("--host", default="127.0.0.1", help="Server host")
@click.option("--port", default=8080, help="Server port")
def serve(host: str, port: int) -> None:
    """Start the API server."""
    click.echo(f"Starting server on {host}:{port}...")
    click.echo("Note: Full implementation coming soon!")
    # TODO: Implement server


if __name__ == "__main__":
    cli()
