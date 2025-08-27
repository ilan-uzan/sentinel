# Sentinel

A lightweight system monitoring tool for process collection and analysis.

## Features

- Process monitoring and collection
- PostgreSQL database storage
- FastAPI web interface (coming soon)
- CLI interface with Typer
- Configurable collection intervals

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ilan-uzan/sentinel.git
cd sentinel
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables for database connection:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=sentinel_one_lite
export DB_USER=solite_user
export DB_PASSWORD=your_password
export COLLECT_INTERVAL_SEC=10
```

## Usage

### CLI Commands

Show status:
```bash
python main.py status
```

Start monitoring:
```bash
python main.py start --interval 30
```

### Development

The project follows a clean architecture pattern:

- `sentinel/` - Main package
  - `core/` - Core business logic
  - `services/` - Business services
  - `storage/` - Database and storage operations
  - `api/` - Web API endpoints (coming soon)
- `main.py` - CLI entry point
- `config.py` - Configuration management

## License

MIT License - see LICENSE file for details. 