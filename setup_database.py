#!/usr/bin/env python3
"""
Database setup script for Sentinel.
Creates tables and inserts sample data.
"""
import psycopg2
import json
from config import settings

def setup_database():
    """Set up the database with tables and sample data."""
    
    # SQL statements
    create_events_table = """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        event_type VARCHAR(50) NOT NULL,
        data JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_alerts_table = """
    CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        severity VARCHAR(50) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
        details JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_indexes = """
    CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
    CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
    CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at DESC);
    """
    
    sample_events = [
        ('system', {'message': 'System startup', 'uptime': 0}),
        ('process', {'pid': 1, 'name': 'systemd', 'cpu_percent': 0.1}),
        ('network', {'local_addr': '127.0.0.1:22', 'remote_addr': '192.168.1.100:12345', 'status': 'ESTABLISHED'})
    ]
    
    sample_alerts = [
        ('Suspicious Network Connection', 'medium', {'ip': '192.168.1.100', 'reason': 'Blocklisted IP detected'}),
        ('High CPU Usage', 'low', {'process': 'python', 'cpu_percent': 85.2})
    ]
    
    try:
        # Connect to database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password
        )
        
        cursor = conn.cursor()
        
        # Create tables
        print("📋 Creating tables...")
        cursor.execute(create_events_table)
        cursor.execute(create_alerts_table)
        
        # Create indexes
        print("🔍 Creating indexes...")
        cursor.execute(create_indexes)
        
        # Commit table creation
        conn.commit()
        print("✅ Tables and indexes created successfully!")
        
        # Insert sample data
        print("📝 Inserting sample data...")
        for event_type, data in sample_events:
            cursor.execute(
                "INSERT INTO events (event_type, data) VALUES (%s, %s)",
                (event_type, json.dumps(data))
            )
        
        for title, severity, details in sample_alerts:
            cursor.execute(
                "INSERT INTO alerts (title, severity, details) VALUES (%s, %s, %s)",
                (title, severity, json.dumps(details))
            )
        
        conn.commit()
        print("✅ Sample data inserted successfully!")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM events")
        event_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alerts")
        alert_count = cursor.fetchone()[0]
        
        print(f"📊 Events in database: {event_count}")
        print(f"📊 Alerts in database: {alert_count}")
        
        cursor.close()
        conn.close()
        print("🎉 Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_database() 