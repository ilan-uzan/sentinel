#!/usr/bin/env python3
"""
Main entry point for Sentinel API server.
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Sentinel API server...")
    print("📡 API will be available at: http://localhost:8000")
    print("🔍 Health check: http://localhost:8000/health")
    print("📊 Events: http://localhost:8000/events")
    print("🚨 Alerts: http://localhost:8000/alerts")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run("sentinel.api.app:app", host="0.0.0.0", port=8000, reload=True) 