"""
Database connection using psycopg2.
"""
import psycopg2
import json
import sys
import os
from psycopg2.extras import RealDictCursor

# Add root directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


def get_connection():
    """Get a database connection using psycopg2."""
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password
    )


def get_cursor(connection):
    """Get a cursor that returns dictionaries."""
    return connection.cursor(cursor_factory=RealDictCursor) 