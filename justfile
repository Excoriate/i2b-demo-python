# justfile for i2b-demo-python

# 🌍 Load environment variables from .env file automatically
set dotenv-load

# 🐚 Set the default shell to bash with error handling
set shell := ["bash", "-uce"]

# --- Variables ---
SRC_DIR := "src"
APP_MODULE := "src.app.main:app"
DEV_HOST := "0.0.0.0"
DEV_PORT := "8000"
VENV_DIR := ".venv"
UV := "uv"

# --- Recipes ---

# 📋 List available recipes
default:
    @echo "🐍 Python Project Recipes 🚀"
    @echo ""
    @echo "--- Local Development ---"
    @echo "  venv           Create virtual environment using uv (if not exists)"
    @echo "  install        Create venv (if needed) and install dependencies"
    @echo "  sync           Sync environment with pyproject.toml dependencies"
    @echo "  run / serve    Run the development server (uvicorn)"
    @echo "  test           Run tests using pytest"
    @echo "  lint           Run linters (TODO)"
    @echo "  format         Run code formatters (TODO)"
    @echo ""
    @echo "--- Docker Compose ---"
    @echo "  compose-build  Build Docker images for services"
    @echo "  compose-up     Start all services using Docker Compose (detached)"
    @echo "  compose-down   Stop and remove all services, networks, and volumes"
    @echo "  compose-logs   Follow logs for the 'app' service"
    @echo "  db-up          Start only the CouchDB service (detached)"
    @echo "  db-down        Stop only the CouchDB service"
    @echo ""
    @echo "--- Cleanup ---"
    @echo "  clean          Clean Python cache files and build artifacts"
    # @just --list # Alternative way to list recipes

# 📦 Create virtual environment using uv (if not exists)
venv:
    @echo ">>> Checking for virtual environment..."
    @if [ ! -d "{{VENV_DIR}}" ]; then \
        echo "Creating virtual environment in {{VENV_DIR}} using uv..."; \
        {{UV}} venv; \
    else \
        echo "Virtual environment {{VENV_DIR}} already exists."; \
    fi

# ⚙️ Install project dependencies including dev extras
# Depends on the virtual environment being created first.
install: venv
    @echo ">>> Installing dependencies using uv..."
    {{UV}} pip install -e .[dev]

# ✨ Sync environment with pyproject.toml dependencies
# Depends on the virtual environment being created first.
sync: venv
    @echo ">>> Syncing environment using uv..."
    {{UV}} pip sync --all-extras

# 🚀 Run the development server (uvicorn)
# Uses .env variables automatically due to 'set dotenv-load'
run:
    @echo ">>> Starting development server (using settings from .env if available)..."
    {{UV}} run uvicorn {{APP_MODULE}} --host {{DEV_HOST}} --port {{DEV_PORT}} --reload

# Alias for run
serve: run

# 🧪 Run tests using pytest
test:
    @echo ">>> Running tests using pytest..."
    {{UV}} run pytest tests/

#  Linter placeholder (TODO: configure tools like Ruff/MyPy)
lint:
    @echo ">>> Linting (TODO: configure tools like Ruff/MyPy)..."
    # Example: {{UV}} run ruff check {{SRC_DIR}} tests
    # Example: {{UV}} run mypy {{SRC_DIR}}
    @echo "Lint recipe needs configuration."

# Formatter placeholder (TODO: configure tools like Ruff format/Black)
format:
    @echo ">>> Formatting (TODO: configure tools like Ruff format/Black)..."
    # Example: {{UV}} run ruff format {{SRC_DIR}} tests
    @echo "Format recipe needs configuration."

# 🧹 Clean Python cache files and build artifacts
clean-py:
    @echo ">>> Cleaning Python cache files..."
    @find . -type f -name '*.py[co]' -delete
    @find . -type d -name '__pycache__' -exec rm -rf {} +
    @find . -type d -name '.pytest_cache' -exec rm -rf {} +
    @find . -type d -name '.mypy_cache' -exec rm -rf {} +
    @find . -type d -name '.ruff_cache' -exec rm -rf {} +
    @rm -rf build dist *.egg-info htmlcov .coverage

# Alias for Python clean
clean: clean-py


# --- Docker Compose Recipes ---

# 🐳 Build Docker images
compose-build:
    @echo ">>> Building Docker images..."
    @docker compose build

# 🐳 Start services using Docker Compose (detached mode)
compose-up:
    @echo ">>> Starting services with Docker Compose..."
    @docker compose up -d --build

# 🐳 Stop and remove services, networks, and volumes
compose-down:
    @echo ">>> Stopping and removing Docker Compose services..."
    @docker compose down -v

# 🐳 Follow logs for the 'app' service
compose-logs:
    @echo ">>> Following logs for 'app' service (Ctrl+C to stop)..."
    @docker compose logs -f app

# 🐳 Start only the CouchDB service (detached mode)
db-up:
    @echo ">>> Starting CouchDB service..."
    @docker compose up -d db

# 🐳 Stop only the CouchDB service
db-down:
    @echo ">>> Stopping CouchDB service..."
    @docker compose stop db
