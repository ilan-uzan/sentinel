#!/usr/bin/env python3
"""
Main entry point for Sentinel application
"""

import typer
from config import settings

app = typer.Typer(
    name="sentinel",
    help="System monitoring and process collection tool",
    add_completion=False
)

@app.command()
def start(
    interval: int = typer.Option(
        settings.collect_interval_sec,
        "--interval", "-i",
        help="Collection interval in seconds"
    ),
    config_file: str = typer.Option(
        None,
        "--config", "-c",
        help="Path to configuration file"
    )
):
    """Start the Sentinel monitoring service"""
    typer.echo(f"Starting Sentinel with {interval}s collection interval")
    # TODO: Implement monitoring service
    typer.echo("Monitoring service not yet implemented")

@app.command()
def status():
    """Show current system status"""
    typer.echo("Sentinel Status:")
    typer.echo(f"  Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
    typer.echo(f"  Collection Interval: {settings.collect_interval_sec}s")

if __name__ == "__main__":
    app() 