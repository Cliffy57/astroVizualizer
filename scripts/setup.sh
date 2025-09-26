# scripts/setup.sh
#!/bin/bash
# Setup script for AstroViz development environment

set -e

echo "🚀 Setting up AstroViz development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -e ".[dev,docs]"

# Setup pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cat > .env << EOF
NASA_API_KEY=DEMO_KEY
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_CONCURRENT_REQUESTS=10
EOF
    echo "📝 Please edit .env with your NASA API key"
fi

# Run initial tests
echo "🧪 Running initial tests..."
pytest tests/ -v

echo "🎉 Setup complete! Activate the environment with:"
echo "   source .venv/bin/activate"
echo "🚀 Start the server with:"
echo "   python -m astroviz.api.main"

# scripts/run_tests.sh
#!/bin/bash
# Comprehensive test runner script

set -e

echo "🧪 Running AstroViz test suite..."

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

# Run code formatting check
echo "🎨 Checking code formatting..."
ruff format --check .

# Run linting
echo "🔍 Running linter..."
ruff check .

# Run type checking
echo "🔒 Running type checks..."
mypy src/astroviz/

# Run tests with coverage
echo "🧪 Running tests with coverage..."
pytest tests/ \
    --cov=src/astroviz \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v

echo "✅ All tests passed!"
echo "📊 Coverage report generated in htmlcov/"

# Makefile
.PHONY: help install dev test lint format type-check docs clean run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -e .

dev: ## Install development dependencies
	pip install -e ".[dev,docs]"
	pre-commit install

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=src/astroviz --cov-report=term-missing --cov-report=html

lint: ## Run linter
	ruff check .

format: ## Format code
	ruff format .

format-check: ## Check code formatting
	ruff format --check .

type-check: ## Run type checker
	mypy src/astroviz/

quality: format lint type-check ## Run all code quality checks

docs: ## Build documentation
	cd docs && make html

docs-serve: ## Serve documentation with auto-reload
	cd docs && sphinx-autobuild . _build/html

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run: ## Run development server
	python -m astroviz.api.main

docker-build: ## Build Docker image
	docker build -t astroviz:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 astroviz:latest

# Dockerfile
FROM python:3.11-slim

LABEL maintainer="Cliffy57"
LABEL description="AstroViz - Professional asteroid data visualization platform"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r astroviz && useradd -r -g astroviz astroviz

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install .

# Copy application code
COPY src/ src/
COPY README.md .

# Change ownership to non-root user
RUN chown -R astroviz:astroviz /app
USER astroviz

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "astroviz.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml
version: '3.8'

services:
  astroviz:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NASA_API_KEY=${NASA_API_KEY:-DEMO_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev,docs]"

    - name: Format check
      run: ruff format --check .

    - name: Lint
      run: ruff check .

    - name: Type check
      run: mypy src/astroviz/

    - name: Test
      run: pytest tests/ --cov=src/astroviz --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[docs]"

    - name: Build docs
      run: |
        cd docs
        make html
