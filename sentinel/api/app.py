"""
FastAPI application with health, events, and alerts endpoints.
"""
from fastapi import FastAPI, Query
from typing import List, Dict, Any
from ..storage.repositories import EventRepository, AlertRepository

app = FastAPI(
    title="Sentinel API",
    description="System monitoring and alerting API",
    version="0.1.0"
)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Status response
    """
    return {"status": "ok"}


@app.get("/events")
async def get_events(limit: int = Query(20, ge=1, le=100)) -> List[Dict[str, Any]]:
    """
    Get latest events.
    
    Args:
        limit: Maximum number of events to return (1-100)
        
    Returns:
        List[Dict[str, Any]]: List of event dictionaries
    """
    # TODO: Implement events endpoint
    # Pseudocode:
    # 1. Call EventRepository.latest(limit)
    # 2. Return events list
    return []


@app.get("/alerts")
async def get_alerts(limit: int = Query(20, ge=1, le=100)) -> List[Dict[str, Any]]:
    """
    Get latest alerts.
    
    Args:
        limit: Maximum number of alerts to return (1-100)
        
    Returns:
        List[Dict[str, Any]]: List of alert dictionaries
    """
    # TODO: Implement alerts endpoint
    # Pseudocode:
    # 1. Call AlertRepository.latest(limit)
    # 2. Return alerts list
    return [] 