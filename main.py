#!/usr/bin/env python3
"""
Enhanced main entry point for Sentinel API server.
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Sentinel API Server v1.0.0...")
    print("=" * 60)
    print("📡 API will be available at: http://localhost:8000")
    print("📚 Interactive API docs: http://localhost:8000/docs")
    print("📖 Alternative docs: http://localhost:8000/redoc")
    print("=" * 60)
    print("🔍 Core Endpoints:")
    print("  • GET  /health     - System health check")
    print("  • GET  /status     - Comprehensive system status")
    print("  • GET  /events     - System events with filtering")
    print("  • GET  /alerts     - Security alerts with filtering")
    print("=" * 60)
    print("🚀 Advanced Features:")
    print("  • POST /scan       - Manual system scan")
    print("  • GET  /monitor    - Real-time monitoring stream")
    print("  • GET  /rules      - Security rules configuration")
    print("  • POST /rules/reload - Reload security rules")
    print("  • GET  /stats      - System statistics")
    print("  • GET  /processes  - Process information with sorting")
    print("  • GET  /network    - Network connections")
    print("=" * 60)
    print("⚡ Real-time Features:")
    print("  • Server-Sent Events for live monitoring")
    print("  • Background task processing")
    print("  • CORS enabled for web integration")
    print("  • Comprehensive error handling")
    print("=" * 60)
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 60)

    uvicorn.run(
        "sentinel.api.app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 