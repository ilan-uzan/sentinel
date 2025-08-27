"""
Data structures for events and alerts (no SQLAlchemy).
"""
from datetime import datetime, timezone
from typing import Dict, Any


class Event:
    """
    Data structure for system events.
    
    Events represent collected system data from various collectors.
    """
    
    def __init__(self, event_type: str, data: Dict[str, Any], created_at: datetime = None):
        self.event_type = event_type
        self.data = data
        self.created_at = created_at or datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database insertion."""
        return {
            'event_type': self.event_type,
            'data': self.data,
            'created_at': self.created_at
        }


class Alert:
    """
    Data structure for security alerts.
    
    Alerts are generated when events match rule conditions.
    """
    
    def __init__(self, title: str, severity: str, details: Dict[str, Any], created_at: datetime = None):
        self.title = title
        self.severity = severity
        self.details = details
        self.created_at = created_at or datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database insertion."""
        return {
            'title': self.title,
            'severity': self.severity,
            'details': self.details,
            'created_at': self.created_at
        } 