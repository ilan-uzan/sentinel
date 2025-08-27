"""
Enhanced FastAPI application with comprehensive monitoring and alerting endpoints.
"""
import sys
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Query, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import asyncio

# Add root directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentinel.storage.repositories import EventRepository, AlertRepository
from sentinel.core.process_collector import ProcessCollector
from sentinel.core.network_collector import NetworkCollector
from sentinel.services.collector_service import CollectorService
from sentinel.services.rule_engine import RuleEngine
from config import settings

app = FastAPI(
    title="Sentinel API",
    description="Advanced System Monitoring and Alerting API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instances
collector_service = None
rule_engine = None

def get_collector_service():
    """Dependency to get collector service instance."""
    global collector_service
    if collector_service is None:
        collectors = [ProcessCollector(), NetworkCollector()]
        collector_service = CollectorService(collectors)
    return collector_service

def get_rule_engine():
    """Dependency to get rule engine instance."""
    global rule_engine
    if rule_engine is None:
        rule_engine = RuleEngine()
    return rule_engine

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global collector_service, rule_engine
    collectors = [ProcessCollector(), NetworkCollector()]
    collector_service = CollectorService(collectors)
    rule_engine = RuleEngine()
    print("🚀 Sentinel API started successfully!")

@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint with API information.
    """
    return {
        "name": "Sentinel API",
        "version": "1.0.0",
        "description": "Advanced System Monitoring and Alerting API",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "events": "/events",
            "alerts": "/alerts",
            "scan": "/scan",
            "monitor": "/monitor",
            "rules": "/rules",
            "stats": "/stats"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Enhanced health check endpoint.
    Returns:
        Dict[str, Any]: Comprehensive health status
    """
    try:
        # Check database connectivity
        db_status = "healthy"
        try:
            EventRepository.latest(1)
        except Exception:
            db_status = "unhealthy"
        
        # Check collector service
        collector_status = "healthy"
        try:
            service = get_collector_service()
            collector_status = service.get_collector_status()
        except Exception:
            collector_status = "unhealthy"
        
        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "components": {
                "database": db_status,
                "collectors": collector_status,
                "rule_engine": "healthy" if rule_engine else "unhealthy"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/status")
async def system_status() -> Dict[str, Any]:
    """
    Comprehensive system status endpoint.
    Returns:
        Dict[str, Any]: Complete system status
    """
    try:
        service = get_collector_service()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "collectors": service.get_collector_status(),
            "rules": service.get_rule_engine_status(),
            "configuration": {
                "db_host": settings.db_host,
                "db_port": settings.db_port,
                "db_name": settings.db_name,
                "collection_interval": settings.collect_interval_sec
            },
            "recent_data": {
                "events_count": len(EventRepository.latest(5)),
                "alerts_count": len(AlertRepository.latest(5))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.get("/events")
async def get_events(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of events to return"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity level")
) -> List[Dict[str, Any]]:
    """
    Get latest events with optional filtering.
    Args:
        limit: Maximum number of events to return (1-100)
        event_type: Filter by event type (process, network)
        severity: Filter by severity level
    Returns:
        List[Dict[str, Any]]: List of filtered event dictionaries
    """
    try:
        events = EventRepository.latest(limit)
        
        # Apply filters
        if event_type:
            events = [e for e in events if e.get('event_type') == event_type]
        
        if severity:
            events = [e for e in events if e.get('data', {}).get('severity') == severity]
        
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch events: {str(e)}")

@app.get("/alerts")
async def get_alerts(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of alerts to return"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    active: Optional[bool] = Query(True, description="Show only active alerts")
) -> List[Dict[str, Any]]:
    """
    Get latest alerts with optional filtering.
    Args:
        limit: Maximum number of alerts to return (1-100)
        severity: Filter by severity level (low, medium, high, critical)
        active: Show only active alerts
    Returns:
        List[Dict[str, Any]]: List of filtered alert dictionaries
    """
    try:
        alerts = AlertRepository.latest(limit)
        
        # Apply filters
        if severity:
            alerts = [a for a in alerts if a.get('severity') == severity]
        
        if active:
            # Consider alerts from last 24 hours as active
            cutoff_time = datetime.now(timezone.utc).timestamp() - 86400
            alerts = [a for a in alerts if a.get('created_at', 0) > cutoff_time]
        
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

@app.post("/scan")
async def manual_scan(
    background_tasks: BackgroundTasks,
    service: CollectorService = Depends(get_collector_service)
) -> Dict[str, Any]:
    """
    Trigger a manual system scan.
    Returns:
        Dict[str, Any]: Scan results and status
    """
    try:
        # Perform scan
        events, alerts = service.collect_and_alert()
        
        # Store events
        from sentinel.storage.models import Event
        event_models = [Event(event['event_type'], event) for event in events]
        events_stored = EventRepository.insert_many(event_models)
        
        # Store alerts
        alerts_stored = 0
        if alerts:
            for alert in alerts:
                if AlertRepository.insert(alert['title'], alert['severity'], alert['details']):
                    alerts_stored += 1
        
        return {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scan_results": {
                "events_collected": len(events),
                "events_stored": events_stored,
                "alerts_generated": len(alerts),
                "alerts_stored": alerts_stored
            },
            "event_types": list(set(event.get('event_type') for event in events))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.get("/monitor")
async def real_time_monitor(
    duration: int = Query(60, ge=10, le=300, description="Monitoring duration in seconds")
) -> StreamingResponse:
    """
    Real-time monitoring stream.
    Args:
        duration: Monitoring duration in seconds (10-300)
    Returns:
        StreamingResponse: Real-time data stream
    """
    async def generate_monitoring_data():
        """Generate real-time monitoring data."""
        service = get_collector_service()
        start_time = datetime.now(timezone.utc)
        end_time = start_time.timestamp() + duration
        
        while datetime.now(timezone.utc).timestamp() < end_time:
            try:
                # Collect current data
                events, alerts = service.collect_and_alert()
                
                # Create monitoring snapshot
                snapshot = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "events_count": len(events),
                    "alerts_count": len(alerts),
                    "system_status": service.get_collector_status(),
                    "top_processes": sorted(
                        [e for e in events if e.get('event_type') == 'process'],
                        key=lambda x: x.get('data', {}).get('cpu_percent', 0),
                        reverse=True
                    )[:5],
                    "network_connections": len([e for e in events if e.get('event_type') == 'network'])
                }
                
                # Send data as Server-Sent Events
                yield f"data: {json.dumps(snapshot)}\n\n"
                
                # Wait before next collection
                await asyncio.sleep(5)
                
            except Exception as e:
                error_data = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "error": str(e),
                    "status": "error"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                await asyncio.sleep(5)
    
    return StreamingResponse(
        generate_monitoring_data(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

@app.get("/rules")
async def get_rules(
    service: CollectorService = Depends(get_collector_service)
) -> Dict[str, Any]:
    """
    Get current security rules configuration.
    Returns:
        Dict[str, Any]: Rules configuration and status
    """
    try:
        return service.get_rule_engine_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch rules: {str(e)}")

@app.post("/rules/reload")
async def reload_rules(
    service: CollectorService = Depends(get_collector_service)
) -> Dict[str, Any]:
    """
    Reload security rules from configuration file.
    Returns:
        Dict[str, Any]: Reload status
    """
    try:
        success = service.reload_rules()
        return {
            "status": "success" if success else "failed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "Rules reloaded successfully" if success else "Failed to reload rules"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rules reload failed: {str(e)}")

@app.get("/stats")
async def get_statistics(
    hours: int = Query(24, ge=1, le=168, description="Statistics period in hours")
) -> Dict[str, Any]:
    """
    Get system statistics for the specified period.
    Args:
        hours: Statistics period in hours (1-168)
    Returns:
        Dict[str, Any]: System statistics
    """
    try:
        # Get recent events and alerts
        recent_events = EventRepository.latest(1000)  # Get more for statistics
        recent_alerts = AlertRepository.latest(1000)
        
        # Calculate time cutoff
        cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
        
        # Filter by time - handle both datetime objects and timestamps
        def is_recent(item):
            created_at = item.get('created_at')
            if isinstance(created_at, datetime):
                return created_at.timestamp() > cutoff_time
            elif isinstance(created_at, (int, float)):
                return created_at > cutoff_time
            return False
        
        period_events = [e for e in recent_events if is_recent(e)]
        period_alerts = [a for a in recent_alerts if is_recent(a)]
        
        # Calculate statistics
        event_types = {}
        alert_severities = {}
        
        for event in period_events:
            event_type = event.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        for alert in period_alerts:
            severity = alert.get('severity', 'unknown')
            alert_severities[severity] = alert_severities.get(severity, 0) + 1
        
        return {
            "period_hours": hours,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "statistics": {
                "total_events": len(period_events),
                "total_alerts": len(period_alerts),
                "event_distribution": event_types,
                "alert_distribution": alert_severities,
                "events_per_hour": len(period_events) / hours if hours > 0 else 0,
                "alerts_per_hour": len(period_alerts) / hours if hours > 0 else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics calculation failed: {str(e)}")

@app.get("/processes")
async def get_processes(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of processes to return"),
    sort_by: str = Query("cpu", description="Sort by: cpu, memory, pid, name")
) -> List[Dict[str, Any]]:
    """
    Get current system processes with sorting options.
    Args:
        limit: Maximum number of processes to return
        sort_by: Sort field (cpu, memory, pid, name)
    Returns:
        List[Dict[str, Any]]: List of process information
    """
    try:
        # Get recent process events
        events = EventRepository.latest(1000)
        process_events = [e for e in events if e.get('event_type') == 'process']
        
        # Sort processes
        if sort_by == "cpu":
            process_events.sort(key=lambda x: x.get('data', {}).get('cpu_percent', 0), reverse=True)
        elif sort_by == "memory":
            process_events.sort(key=lambda x: x.get('data', {}).get('memory_mb', 0), reverse=True)
        elif sort_by == "pid":
            process_events.sort(key=lambda x: x.get('data', {}).get('pid', 0))
        elif sort_by == "name":
            process_events.sort(key=lambda x: x.get('data', {}).get('name', ''))
        
        return process_events[:limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch processes: {str(e)}")

@app.get("/network")
async def get_network_connections(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of connections to return")
) -> List[Dict[str, Any]]:
    """
    Get current network connections.
    Args:
        limit: Maximum number of connections to return
    Returns:
        List[Dict[str, Any]]: List of network connection information
    """
    try:
        # Get recent network events
        events = EventRepository.latest(1000)
        network_events = [e for e in events if e.get('event_type') == 'network']
        
        return network_events[:limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch network connections: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 