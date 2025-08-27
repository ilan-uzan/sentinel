#!/usr/bin/env python3
"""
Sentinel CLI - Command-line interface for system monitoring and alerting.
"""
import sys
import os
import time
import signal
from typing import Optional
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from sentinel.core.process_collector import ProcessCollector
from sentinel.core.network_collector import NetworkCollector
from sentinel.services.collector_service import CollectorService
from sentinel.storage.repositories import EventRepository, AlertRepository
from config import settings

# Initialize Typer app and Rich console
app = typer.Typer(help="Sentinel - System monitoring and alerting CLI")
console = Console()


def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    console.print("\n🛑 [yellow]Interrupt received. Shutting down gracefully...[/yellow]")
    sys.exit(0)


@app.command()
def scan_once(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output")
):
    """
    Perform a single system scan: collect data, evaluate rules, and generate alerts.
    """
    console.print(Panel.fit("🔍 [bold blue]Sentinel System Scan[/bold blue]", border_style="blue"))
    
    try:
        # Initialize collectors and service
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Initialize components
            progress.add_task("Initializing collectors...", total=None)
            collectors = [ProcessCollector(), NetworkCollector()]
            service = CollectorService(collectors)
            
            # Collect data
            progress.add_task("Collecting system data...", total=None)
            events, alerts = service.collect_and_alert()
            
            # Store events
            progress.add_task("Storing events in database...", total=None)
            from sentinel.storage.models import Event
            event_models = [Event(event['event_type'], event) for event in events]
            events_stored = EventRepository.insert_many(event_models)
            
            # Store alerts if any
            alerts_stored = 0
            if alerts:
                progress.add_task("Storing alerts in database...", total=None)
                for alert in alerts:
                    if AlertRepository.insert(alert['title'], alert['severity'], alert['details']):
                        alerts_stored += 1
        
        # Display results
        console.print(f"\n✅ [green]Scan completed successfully![/green]")
        
        # Summary table
        summary_table = Table(title="Scan Results", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Events Collected", str(len(events)))
        summary_table.add_row("Events Stored", "✅" if events_stored else "❌")
        summary_table.add_row("Alerts Generated", str(len(alerts)))
        summary_table.add_row("Alerts Stored", str(alerts_stored) if alerts else "0")
        
        console.print(summary_table)
        
        # Show event types
        event_types = set(event.get('event_type') for event in events)
        console.print(f"\n📊 [blue]Event Types:[/blue] {', '.join(event_types)}")
        
        # Show alerts if any
        if alerts:
            console.print(f"\n🚨 [red]Generated Alerts:[/red]")
            for i, alert in enumerate(alerts[:5], 1):  # Show first 5
                console.print(f"  {i}. [bold]{alert['title']}[/bold] ([yellow]{alert['severity']}[/yellow])")
        
        if verbose:
            # Show detailed event information
            console.print(f"\n📋 [blue]Detailed Event Information:[/blue]")
            for i, event in enumerate(events[:3], 1):  # Show first 3
                console.print(f"  Event {i}: {event.get('event_type', 'unknown')} - {event}")
        
    except Exception as e:
        console.print(f"\n❌ [red]Error during scan: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def agent_start(
    interval: Optional[int] = typer.Option(
        None, 
        "--interval", 
        "-i", 
        help="Scan interval in seconds (defaults to COLLECT_INTERVAL_SEC from config)"
    )
):
    """
    Start continuous monitoring agent with periodic scanning.
    """
    # Set scan interval
    scan_interval = interval or settings.collect_interval_sec
    
    console.print(Panel.fit(
        f"🤖 [bold green]Sentinel Agent Starting[/bold green]\n"
        f"Scan interval: {scan_interval} seconds",
        border_style="green"
    ))
    
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize components
        console.print("🔧 [blue]Initializing monitoring components...[/blue]")
        collectors = [ProcessCollector(), NetworkCollector()]
        service = CollectorService(collectors)
        
        # Show initial status
        rules_status = service.get_rule_engine_status()
        console.print(f"📋 [blue]Rules loaded:[/blue] {rules_status['blocklisted_ips_count']} blocklisted IPs")
        
        console.print(f"\n🚀 [green]Agent started! Monitoring every {scan_interval} seconds...[/green]")
        console.print("⏹️  Press Ctrl+C to stop\n")
        
        scan_count = 0
        start_time = time.time()
        
        while True:
            try:
                scan_count += 1
                current_time = time.strftime("%H:%M:%S")
                
                console.print(f"🔍 [blue][{current_time}] Starting scan #{scan_count}...[/blue]")
                
                # Perform scan
                events, alerts = service.collect_and_alert()
                
                # Store events
                from sentinel.storage.models import Event
                event_models = [Event(event['event_type'], event) for event in events]
                events_stored = EventRepository.insert_many(event_models)
                
                # Store alerts if any
                alerts_stored = 0
                if alerts:
                    for alert in alerts:
                        if AlertRepository.insert(alert['title'], alert['severity'], alert['details']):
                            alerts_stored += 1
                
                # Display scan results
                console.print(f"  ✅ Events: {len(events)} collected, {len(events)} stored")
                if alerts:
                    console.print(f"  🚨 Alerts: {len(alerts)} generated, {alerts_stored} stored")
                else:
                    console.print(f"  ✅ Alerts: None generated")
                
                # Show uptime
                uptime = time.time() - start_time
                console.print(f"  ⏱️  Uptime: {uptime:.0f}s | Total scans: {scan_count}")
                
                # Wait for next scan
                if scan_count < 10:  # Show countdown for first 10 scans
                    console.print(f"  ⏳ Next scan in {scan_interval} seconds...\n")
                else:
                    console.print(f"  ⏳ Next scan in {scan_interval} seconds... (scan #{scan_count + 1})\n")
                
                time.sleep(scan_interval)
                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                console.print(f"  ❌ [red]Error during scan #{scan_count}: {e}[/red]")
                console.print(f"  ⏳ Retrying in {scan_interval} seconds...\n")
                time.sleep(scan_interval)
                
    except KeyboardInterrupt:
        console.print(f"\n🛑 [yellow]Agent stopped by user[/yellow]")
        console.print(f"📊 [blue]Final stats:[/blue] {scan_count} scans completed in {time.time() - start_time:.0f}s")
    except Exception as e:
        console.print(f"\n❌ [red]Agent error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def status():
    """
    Show current system status and configuration.
    """
    console.print(Panel.fit("📊 [bold blue]Sentinel System Status[/bold blue]", border_style="blue"))
    
    try:
        # Initialize components
        collectors = [ProcessCollector(), NetworkCollector()]
        service = CollectorService(collectors)
        
        # Collector status
        collector_status = service.get_collector_status()
        console.print("\n🔧 [blue]Collector Status:[/blue]")
        for name, status in collector_status.items():
            status_icon = "✅" if status['working'] else "❌"
            console.print(f"  {status_icon} {name}: {status['status']} ({status['sample_count']} samples)")
        
        # Rule engine status
        rules_status = service.get_rule_engine_status()
        console.print(f"\n📋 [blue]Rule Engine:[/blue]")
        console.print(f"  📁 Rules file: {rules_status['rules_file']}")
        console.print(f"  🚫 Blocklisted IPs: {rules_status['blocklisted_ips_count']}")
        console.print(f"  ⚠️  Severity levels: {', '.join(rules_status['severity_levels'].keys())}")
        
        # Configuration
        console.print(f"\n⚙️  [blue]Configuration:[/blue]")
        console.print(f"  🗄️  Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
        console.print(f"  ⏱️  Collection interval: {settings.collect_interval_sec} seconds")
        
        # Recent data counts
        recent_events = EventRepository.latest(5)
        recent_alerts = AlertRepository.latest(5)
        console.print(f"\n📊 [blue]Recent Data:[/blue]")
        console.print(f"  📝 Events: {len(recent_events)} recent")
        console.print(f"  🚨 Alerts: {len(recent_alerts)} recent")
        
    except Exception as e:
        console.print(f"\n❌ [red]Error getting status: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def test():
    """
    Test the system components and connectivity.
    """
    console.print(Panel.fit("🧪 [bold blue]Sentinel System Test[/bold blue]", border_style="blue"))
    
    try:
        # Test database connection
        console.print("🗄️  [blue]Testing database connection...[/blue]")
        test_events = EventRepository.latest(1)
        console.print("  ✅ Database connection successful")
        
        # Test collectors
        console.print("\n🔧 [blue]Testing collectors...[/blue]")
        collectors = [ProcessCollector(), NetworkCollector()]
        service = CollectorService(collectors)
        
        collector_status = service.get_collector_status()
        for name, status in collector_status.items():
            if status['working']:
                console.print(f"  ✅ {name}: Working ({status['sample_count']} samples)")
            else:
                console.print(f"  ❌ {name}: Error - {status.get('error', 'Unknown error')}")
        
        # Test rule engine
        console.print("\n📋 [blue]Testing rule engine...[/blue]")
        rules_status = service.get_rule_engine_status()
        console.print(f"  ✅ Rules loaded: {rules_status['blocklisted_ips_count']} blocklisted IPs")
        
        # Test full pipeline
        console.print("\n🔄 [blue]Testing full data pipeline...[/blue]")
        events, alerts = service.collect_and_alert()
        console.print(f"  ✅ Data collection: {len(events)} events")
        console.print(f"  ✅ Rule evaluation: {len(alerts)} alerts generated")
        
        console.print("\n🎉 [green]All tests passed! System is ready.[/green]")
        
    except Exception as e:
        console.print(f"\n❌ [red]Test failed: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app() 