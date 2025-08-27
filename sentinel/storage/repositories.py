"""
Data access layer using psycopg2.
"""
import json
import sys
import os
from typing import List, Dict, Any

# Add root directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentinel.storage.db import get_connection, get_cursor
from sentinel.storage.models import Event, Alert


class EventRepository:
    """Repository for event data operations."""
    
    @staticmethod
    def insert_many(events: List[Event]) -> bool:
        """
        Insert multiple events into the database.
        
        Args:
            events: List of Event objects to insert
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            
            for event in events:
                cursor.execute(
                    "INSERT INTO events (event_type, data, created_at) VALUES (%s, %s, %s)",
                    (event.event_type, json.dumps(event.data), event.created_at)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error inserting events: {e}")
            return False
    
    @staticmethod
    def latest(limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get latest events from the database.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List[Dict[str, Any]]: List of event dictionaries
        """
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            
            cursor.execute(
                "SELECT * FROM events ORDER BY created_at DESC LIMIT %s",
                (limit,)
            )
            
            events = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Convert to list of dicts
            return [dict(event) for event in events]
            
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []


class AlertRepository:
    """Repository for alert data operations."""
    
    @staticmethod
    def insert(title: str, severity: str, details: Dict[str, Any]) -> bool:
        """
        Insert a new alert into the database.
        
        Args:
            title: Alert title
            severity: Alert severity level
            details: Alert details dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            
            cursor.execute(
                "INSERT INTO alerts (title, severity, details) VALUES (%s, %s, %s)",
                (title, severity, json.dumps(details))
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error inserting alert: {e}")
            return False
    
    @staticmethod
    def latest(limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get latest alerts from the database.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List[Dict[str, Any]]: List of alert dictionaries
        """
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            
            cursor.execute(
                "SELECT * FROM alerts ORDER BY created_at DESC LIMIT %s",
                (limit,)
            )
            
            alerts = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Convert to list of dicts
            return [dict(alert) for alert in alerts]
            
        except Exception as e:
            print(f"Error fetching alerts: {e}")
            return [] 