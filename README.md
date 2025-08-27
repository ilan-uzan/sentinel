# Sentinel

## 📖 Project Overview

Sentinel is a **minimal, functional cybersecurity monitoring tool** that provides real-time system monitoring and alerting capabilities. The application addresses the need for continuous system surveillance by collecting system data, storing events in a PostgreSQL database, and exposing a RESTful API for monitoring and alert management.

**Problem**: Organizations need a lightweight, local agent for system monitoring without complex enterprise solutions.

**Solution**: A Python-based monitoring tool that collects system data, evaluates security rules, and provides real-time alerts through a simple HTTP API.

**Tech Stack**: Python 3.x with OOP principles, FastAPI, PostgreSQL, and psycopg2 for database operations.

**Use Cases**: Local system monitoring, security event collection, network connection tracking, and process monitoring for development and small-scale deployments.

---

## 🚀 Features

### ✅ Implemented & Working
- **Real Process Monitoring**: Collects actual system processes using psutil (400+ processes)
- **Health Monitoring API**: `/health` endpoint for system status
- **Event Collection**: `/events` endpoint to retrieve system events with pagination
- **Alert Management**: `/alerts` endpoint to view security alerts with severity levels
- **Database Integration**: PostgreSQL with JSONB storage for flexible data
- **Configuration Management**: Environment-based configuration with .env support
- **Auto-reload Development Server**: Hot-reload for development
- **Real Data Pipeline**: Collectors → Database → API working end-to-end

### 🔄 Planned
- **Network Collector**: Network connection monitoring (basic structure ready)
- **Rule Engine**: Automated alert generation (basic structure ready)
- **CLI Interface**: Command-line tools for system administration
- **Real-time Data Collection**: Continuous system monitoring with configurable intervals

---

## 🛠 Tech Stack

- **Programming Language**: Python 3.x with Object-Oriented Programming
- **Database**: PostgreSQL with psycopg2 direct connection
- **Libraries**:
  - `fastapi` - Modern web framework for building APIs
  - `uvicorn` - ASGI server for running FastAPI applications
  - `psycopg2-binary` - PostgreSQL adapter for Python
  - `pydantic` - Data validation using Python type annotations
  - `python-dotenv` - Environment variable management
  - `psutil` - Cross-platform library for system monitoring
  - `typer` - Command-line interface creation
- **APIs**: RESTful HTTP API with JSON responses
- **Architecture**: Clean architecture with separation of concerns (core, services, storage, api)

---

## 📂 Project Structure

```
hackathon/
├── .git/                           # Git repository
├── .gitignore                      # Python .gitignore patterns
├── .venv/                          # Virtual environment
├── LICENSE                         # MIT License
├── README.md                       # Project documentation
├── config.py                       # Configuration management with Pydantic
├── main.py                         # FastAPI server entry point
├── requirements.txt                # Python dependencies
├── database/
│   └── schema.sql                 # PostgreSQL schema with events/alerts tables
├── rules/
│   └── default.json               # Security rules configuration
└── sentinel/                       # Main Python package
    ├── __init__.py                 # Package initialization
    ├── api/                        # HTTP API layer
    │   ├── __init__.py
    │   └── app.py                  # FastAPI application with 3 working endpoints
    ├── core/                       # Core domain logic and collectors
    │   ├── __init__.py
    │   ├── base_collector.py       # Abstract base class for collectors
    │   ├── process_collector.py    # Real process monitoring using psutil
    │   └── network_collector.py    # Network monitoring collector (basic structure)
    ├── services/                   # Business logic and orchestration
    │   ├── __init__.py
    │   ├── collector_service.py    # Working collector orchestration service
    │   └── rule_engine.py          # Basic rule evaluation structure
    └── storage/                    # Database layer and data persistence
        ├── __init__.py
        ├── db.py                   # psycopg2 database connection
        ├── models.py               # Data structures for events and alerts
        └── repositories.py         # Working data access layer with CRUD operations
```

---

## ⚡️ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/ilan-uzan/sentinel.git
cd sentinel
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL
Based on the existing database schema and configuration:

1. **Create Database**: Create a PostgreSQL database named `sentinel_one_lite`
2. **Create User**: Create user `solite_user` with appropriate permissions
3. **Environment Variables**: Create a `.env` file with:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=sentinel_one_lite
   DB_USER=solite_user
   DB_PASSWORD=your_password
   COLLECT_INTERVAL_SEC=10
   ```
4. **Run Schema**: Execute `database/schema.sql` to create tables and indexes

### 4. Run the app
```bash
python3 main.py
```

The API server will start on `http://localhost:8000` with the following endpoints:
- **Health Check**: `GET /health` → `{"status": "ok"}`
- **Events**: `GET /events?limit=20` → Real system process data
- **Alerts**: `GET /alerts?limit=20` → Security alerts from database

---

## 🎯 Roadmap

Based on current implementation status:

### Phase 1: Core Collectors ✅ COMPLETED
- [x] Implement `ProcessCollector.collect()` method using psutil
- [x] Implement `NetworkCollector.collect()` method using psutil
- [x] Complete `CollectorService.collect_all()` orchestration

### Phase 2: Rule Engine 🔄 IN PROGRESS
- [x] Basic `RuleEngine.evaluate_events()` structure
- [ ] Implement actual security rule evaluation logic
- [ ] Integrate with blocklisted IPs from `rules/default.json`

### Phase 3: CLI Interface 🔄 PLANNED
- [ ] Implement `scan_once` command for single system scan
- [ ] Implement `agent_start` command for continuous monitoring
- [ ] Add command-line argument parsing and help

### Phase 4: Enhanced API 🔄 PLANNED
- [ ] Add POST endpoints for manual event/alert creation
- [ ] Implement real-time data streaming
- [ ] Add authentication and rate limiting

---

## 🤝 Contributing

### Branching Model
- **Feature Branches**: Use `feat/<feature-name>` format
- **Never commit directly to main**: All changes go through feature branches
- **Small PRs**: Keep pull requests focused and manageable
- **Merge Strategy**: Feature branches are merged into main after review

### Commit Style
- **Format**: `feat: description of changes`
- **Examples**: 
  - `feat: add process collector implementation`
  - `feat: implement rule engine for alerts`
  - `feat: add CLI scan command`

### Testing
- **API Testing**: Test endpoints with curl or Postman
- **Database Testing**: Verify schema and data operations
- **Integration Testing**: Test collector → storage → API flow

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 ilan

---

## 🔧 Development Notes

- **Database**: Using psycopg2 for direct PostgreSQL access
- **API**: FastAPI with automatic OpenAPI documentation
- **Configuration**: Pydantic-based settings with environment variable support
- **Architecture**: Follows OOP principles with abstract base classes and clear separation of concerns
- **Current Status**: **Minimal and functional** - real collectors working, database operational, API serving live data
- **Data Flow**: System processes → Collectors → PostgreSQL → FastAPI → JSON responses 