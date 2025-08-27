"""
Database connection using psycopg2.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings


def get_connection():
    """Get a database connection using psycopg2."""
    # TODO: Implement psycopg2 connection
    # Pseudocode:
    # 1. Use psycopg2.connect() with settings from config
    # 2. Return connection object
    pass


def get_cursor(connection):
    """Get a cursor that returns dictionaries."""
    # TODO: Return cursor with RealDictCursor for dict results
    # Pseudocode:
    # 1. Return connection.cursor(cursor_factory=RealDictCursor)
    pass 