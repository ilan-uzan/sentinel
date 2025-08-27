# 🛡️ Sentinel - Advanced System Monitoring & Alerting

**Sentinel** is a comprehensive cybersecurity monitoring tool that provides real-time system monitoring, security alerting, and threat detection capabilities. Built with Python OOP principles and modern web technologies.

## ✨ **Features**

### 🔍 **Core Monitoring**
- **Real-time Process Monitoring** - Track CPU, memory, and process status
- **Network Connection Analysis** - Monitor active connections and detect suspicious activity
- **Security Rule Engine** - Configurable rules for threat detection
- **Automated Alerting** - Real-time security alerts with severity levels

### 🚀 **Advanced API (v1.0.0)**
- **RESTful API** - Comprehensive HTTP endpoints for all functionality
- **Real-time Streaming** - Server-Sent Events for live monitoring
- **Advanced Filtering** - Query events and alerts by type, severity, and time
- **Background Processing** - Asynchronous task execution
- **CORS Support** - Web frontend integration ready
- **Interactive Documentation** - Auto-generated API docs with Swagger UI

### 🖥️ **Command Line Interface**
- **Interactive CLI** - Rich terminal interface with progress bars
- **Single Scan Mode** - On-demand system analysis
- **Continuous Monitoring** - Background agent with configurable intervals
- **System Testing** - Comprehensive component validation

### 🗄️ **Data Management**
- **PostgreSQL Storage** - Robust data persistence with JSONB support
- **Event Logging** - Comprehensive system event tracking
- **Alert Management** - Security alert storage and retrieval
- **Statistics & Analytics** - Time-based data analysis

## 🏗️ **Architecture**

```
sentinel/
├── api/                    # FastAPI web application
│   ├── app.py            # Enhanced API with 15+ endpoints
│   └── __init__.py
├── core/                  # Data collection layer
│   ├── base_collector.py # Abstract collector interface
│   ├── process_collector.py # System process monitoring
│   ├── network_collector.py # Network connection analysis
│   └── __init__.py
├── services/              # Business logic layer
│   ├── collector_service.py # Data collection orchestration
│   ├── rule_engine.py    # Security rule evaluation
│   └── __init__.py
└── storage/               # Data persistence layer
    ├── db.py             # PostgreSQL connection management
    ├── models.py         # Data structures
    ├── repositories.py   # Data access layer
    └── __init__.py
```

## 🚀 **Quick Start**

### **1. Prerequisites**
```bash
# PostgreSQL database
# Python 3.8+
# Virtual environment
```

### **2. Installation**
```bash
git clone https://github.com/ilan-uzan/sentinel.git
cd sentinel
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Database Setup**
```bash
# Create PostgreSQL database
createdb sentinel_one_lite

# Run schema
psql -d sentinel_one_lite -f database/schema.sql
```

### **4. Configuration**
Create `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sentinel_one_lite
DB_USER=solite_user
DB_PASSWORD=password
COLLECT_INTERVAL_SEC=10
```

### **5. Start the System**

#### **Option A: API Server**
```bash
python3 main.py
# API available at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

#### **Option B: CLI Interface**
```bash
python3 cli.py --help
python3 cli.py status
python3 cli.py scan-once
python3 cli.py agent-start
```

## 📡 **API Endpoints**

### **Core Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and endpoint list |
| `GET` | `/health` | Enhanced system health check |
| `GET` | `/status` | Comprehensive system status |
| `GET` | `/events` | System events with filtering |
| `GET` | `/alerts` | Security alerts with filtering |

### **Advanced Features**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/scan` | Manual system scan |
| `GET` | `/monitor` | Real-time monitoring stream |
| `GET` | `/rules` | Security rules configuration |
| `POST` | `/rules/reload` | Reload security rules |
| `GET` | `/stats` | System statistics (configurable period) |
| `GET` | `/processes` | Process information with sorting |
| `GET` | `/network` | Network connections |

### **Query Parameters**
- **Filtering**: `event_type`, `severity`, `active`
- **Pagination**: `limit` (1-200)
- **Sorting**: `sort_by` (cpu, memory, pid, name)
- **Time-based**: `hours` for statistics
- **Real-time**: `duration` for monitoring streams

## 🖥️ **CLI Commands**

### **Available Commands**
```bash
python3 cli.py scan-once     # Single system scan
python3 cli.py agent-start   # Continuous monitoring
python3 cli.py status        # System status overview
python3 cli.py test          # Component testing
```

### **Command Options**
```bash
# Scan with verbose output
python3 cli.py scan-once --verbose

# Start agent with custom interval
python3 cli.py agent-start --interval 30

# Get help for any command
python3 cli.py --help
python3 cli.py scan-once --help
```

## 🔧 **Configuration**

### **Environment Variables**
| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `DB_NAME` | `sentinel_one_lite` | Database name |
| `DB_USER` | `solite_user` | Database user |
| `DB_PASSWORD` | `password` | Database password |
| `COLLECT_INTERVAL_SEC` | `10` | Data collection interval |

### **Security Rules**
Configure security rules in `rules/default.json`:
```json
{
  "blocklisted_ips": ["192.168.1.100", "10.0.0.50"],
  "severity_levels": {
    "low": "info",
    "medium": "warning", 
    "high": "critical"
  }
}
```

## 🧪 **Testing**

### **API Testing**
```bash
# Start API server
python3 main.py

# In another terminal, test endpoints
python3 test_enhanced_api.py
```

### **CLI Testing**
```bash
# Test all CLI commands
python3 cli.py test
python3 cli.py status
python3 cli.py scan-once --verbose
```

## 📊 **Real-time Features**

### **Live Monitoring**
- **Server-Sent Events** for real-time data streaming
- **Background task processing** for non-blocking operations
- **Configurable monitoring duration** (10-300 seconds)
- **Live system statistics** and process information

### **Data Streaming**
```bash
# Start real-time monitoring (60 seconds)
curl "http://localhost:8000/monitor?duration=60"

# Monitor with custom duration
curl "http://localhost:8000/monitor?duration=120"
```

## 🔒 **Security Features**

### **Threat Detection**
- **IP Blocklisting** - Block suspicious IP addresses
- **Port Monitoring** - Detect connections to suspicious ports
- **Process Analysis** - Identify high CPU/memory usage
- **Network Pattern Recognition** - Detect unusual connection patterns

### **Alert System**
- **Multi-level Severity** - Low, Medium, High, Critical
- **Real-time Generation** - Instant threat notification
- **Persistent Storage** - Historical alert tracking
- **Configurable Rules** - Dynamic security policy updates

## 🚀 **Advanced Usage**

### **Web Integration**
```javascript
// Real-time monitoring with JavaScript
const eventSource = new EventSource('/monitor?duration=300');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('System update:', data);
};
```

### **Custom Rules**
```bash
# Reload security rules without restart
curl -X POST "http://localhost:8000/rules/reload"

# Get current rules configuration
curl "http://localhost:8000/rules"
```

### **Statistics & Analytics**
```bash
# Get 24-hour statistics
curl "http://localhost:8000/stats?hours=24"

# Get 7-day statistics
curl "http://localhost:8000/stats?hours=168"
```

## 📈 **Performance & Scalability**

### **Optimizations**
- **Connection pooling** for database operations
- **Asynchronous processing** for I/O operations
- **Efficient data structures** for large datasets
- **Configurable collection intervals** for resource management

### **Monitoring Capabilities**
- **500+ concurrent processes** monitoring
- **Real-time network analysis** with permission handling
- **Efficient JSONB storage** for flexible data
- **Indexed queries** for fast data retrieval

## 🛠️ **Development**

### **Project Structure**
```
hackathon/
├── sentinel/              # Main Python package
├── database/              # Database schema
├── rules/                 # Security rules
├── cli.py                # Command-line interface
├── main.py               # API server entry point
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### **Adding New Collectors**
```python
from sentinel.core.base_collector import BaseCollector

class CustomCollector(BaseCollector):
    def collect(self) -> List[Dict[str, Any]]:
        # Implement your collection logic
        return []
```

### **Extending Rules Engine**
```python
# Add new rule types in rules/default.json
# Implement evaluation logic in RuleEngine class
```

## 📚 **API Documentation**

### **Interactive Docs**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### **Example Requests**
```bash
# Health check
curl "http://localhost:8000/health"

# Get filtered events
curl "http://localhost:8000/events?event_type=process&limit=10"

# Manual system scan
curl -X POST "http://localhost:8000/scan"

# Get system statistics
curl "http://localhost:8000/stats?hours=48"
```

## 🤝 **Contributing**

### **Development Workflow**
1. **Feature Branches** - Create `feat/<name>` branches
2. **Small PRs** - Keep changes focused and manageable
3. **Testing** - Ensure all components work before merging
4. **Documentation** - Update README and code comments

### **Code Standards**
- **Python OOP** - Use classes and inheritance
- **Type Hints** - Include type annotations
- **Docstrings** - Document all public methods
- **Error Handling** - Graceful error management

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 **Roadmap**

### **Completed Features** ✅
- [x] **Project Scaffold** - Basic structure and configuration
- [x] **Database Layer** - PostgreSQL with psycopg2
- [x] **Data Collectors** - Process and network monitoring
- [x] **Rule Engine** - Security rule evaluation
- [x] **CLI Interface** - Command-line monitoring tools
- [x] **Enhanced API** - Comprehensive REST API v1.0.0

### **Future Enhancements** 🚀
- [ ] **Web Dashboard** - React/Vue frontend
- [ ] **Machine Learning** - Anomaly detection
- [ ] **Distributed Monitoring** - Multi-node support
- [ ] **Alert Notifications** - Email, Slack, webhook integration
- [ ] **Performance Metrics** - Advanced system analytics
- [ ] **Plugin System** - Extensible collector framework

## 🆘 **Support**

### **Troubleshooting**
- **Database Connection**: Check PostgreSQL service and credentials
- **Permission Issues**: Network collection may require elevated privileges on macOS
- **Import Errors**: Ensure virtual environment is activated
- **API Errors**: Check server logs and database connectivity

### **Getting Help**
- **Documentation**: Check this README and API docs
- **Issues**: Report bugs and feature requests
- **Testing**: Use built-in test commands for validation

---

**🚀 Sentinel v1.0.0** - Advanced system monitoring and cybersecurity alerting platform.

*Built with ❤️ using Python, FastAPI, PostgreSQL, and modern web technologies.* 