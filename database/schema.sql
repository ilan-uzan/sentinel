-- Sentinel Database Schema
-- PostgreSQL database schema for system monitoring and alerting

-- Create events table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    details JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at DESC);

-- Insert sample data for testing
INSERT INTO events (event_type, data) VALUES 
    ('system', '{"message": "System startup", "uptime": 0}'),
    ('process', '{"pid": 1, "name": "systemd", "cpu_percent": 0.1}'),
    ('network', '{"local_addr": "127.0.0.1:22", "remote_addr": "192.168.1.100:12345", "status": "ESTABLISHED"}');

INSERT INTO alerts (title, severity, details) VALUES 
    ('Suspicious Network Connection', 'medium', '{"ip": "192.168.1.100", "reason": "Blocklisted IP detected"}'),
    ('High CPU Usage', 'low', '{"process": "python", "cpu_percent": 85.2}');

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON TABLE events TO solite_user;
-- GRANT ALL PRIVILEGES ON TABLE alerts TO solite_user;
-- GRANT USAGE, SELECT ON SEQUENCE events_id_seq TO solite_user;
-- GRANT USAGE, SELECT ON SEQUENCE alerts_id_seq TO solite_user; 