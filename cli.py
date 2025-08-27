"""
Command line interface for Sentinel.
"""
import typer
import time
from typing import Optional
from sentinel.config import settings
from sentinel.services.collector_service import CollectorService
from sentinel.services.rule_engine import RuleEngine
from sentinel.storage.repositories import EventRepository, AlertRepository
from sentinel.core.process_collector import ProcessCollector
from sentinel.core.network_collector import NetworkCollector

app = typer.Typer(
    name="sentinel",
    help="System monitoring and process collection tool",
    add_completion=False
)


@app.command()
def scan_once():
    """Run collectors once, save events, evaluate rules, save alerts."""
    # TODO: Implement single scan
    # Pseudocode:
    # 1. Create collectors: ProcessCollector(), NetworkCollector()
    # 2. Create CollectorService with collectors
    # 3. Call collect_all() to get events
    # 4. Save events with EventRepository.insert_many()
    # 5. Create RuleEngine and evaluate_events()
    # 6. Save alerts with AlertRepository.insert()
    typer.echo("Single scan completed")


@app.command()
def agent_start(
    interval: Optional[int] = typer.Option(
        None,
        "--interval", "-i",
        help="Collection interval in seconds (overrides .env)"
    )
):
    """Start agent mode: continuous scanning every N seconds."""
    # TODO: Implement continuous agent
    # Pseudocode:
    # 1. Get interval from parameter or .env (COLLECT_INTERVAL_SEC)
    # 2. While True:
    #    - Call scan_once() logic
    #    - Sleep for interval seconds
    #    - Handle keyboard interrupt gracefully
    scan_interval = interval or settings.collect_interval_sec
    typer.echo(f"Starting agent with {scan_interval}s interval")
    typer.echo("Agent mode not yet implemented")


if __name__ == "__main__":
    app() 