# AstroViz 🌌

> Professional asteroid data visualization and analysis platform

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy-lang.org/)

AstroViz is a modern, high-performance web application for visualizing and analyzing asteroid data from NASA's APIs. Built with FastAPI, it provides interactive 3D visualizations and comprehensive data analysis tools for Near-Earth Objects (NEOs) and other asteroids.

## ✨ Features

- 🚀 **Real-time NASA Data**: Direct integration with NASA's NEO and SBDB APIs
- 🌍 **Interactive 3D Visualization**: Explore asteroid orbits and positions in space
- 📊 **Data Analytics**: Statistical analysis and filtering of asteroid datasets
- ⚡ **High Performance**: Async FastAPI backend with optimized data processing
- 🔒 **Type Safety**: Full type checking with MyPy and Pydantic models
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 📚 **Documentation**: Auto-generated API docs and Sphinx documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Git
- NASA API Key (optional, but recommended for production use)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd astroviz
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -e ".[dev,docs]"
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Configure NASA API Key** (optional)
   ```bash
   # Create .env file
   echo "NASA_API_KEY=your_api_key_here" > .env
   ```

### Running the Application

1. **Start the development server**
   ```bash
   # From project root
   python -m astroviz.api.main
   # Or
   uvicorn astroviz.api.main:app --reload
   ```

2. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## 🧪 Development

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_nasa_client.py

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=src/astroviz --cov-report=html
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Documentation

```bash
# Generate documentation
cd docs
make html

# Auto-rebuild docs
sphinx-autobuild . _build/html
```

## 📡 API Endpoints

### Asteroids

- `GET /api/v1/asteroids/` - List asteroids with filtering
- `GET /api/v1/asteroids/{id}` - Get asteroid details
- `GET /api/v1/asteroids/{id}/approaches` - Get close approach data

### Visualization

- `GET /api/v1/viz/3d-scene` - Get 3D visualization data
- `GET /api/v1/viz/stats` - Get asteroid statistics

## 🏗️ Architecture

```
astroviz/
├── src/astroviz/
│   ├── api/                 # FastAPI application
│   │   ├── main.py         # App initialization
│   │   └── routes/         # API endpoints
│   ├── data/               # Data processing
│   │   ├── nasa_client.py  # NASA API client
│   │   └── processor.py    # Data analysis
│   ├── models/             # Pydantic models
│   └── visualization/      # 3D viz components
├── tests/                  # Test suite
├── docs/                   # Documentation
└── scripts/               # Utility scripts
```

## 🌟 Tech Stack

- **Backend**: FastAPI, Pydantic, httpx
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly, Three.js (frontend)
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: ruff, mypy, black, pre-commit
- **Documentation**: Sphinx, sphinx-rtd-theme

## 🛡️ Data Sources

- **NASA NEO Web Service**: Near-Earth Object data
- **NASA Small-Body Database**: Detailed orbital and physical data
- **NASA CNEOS**: Close approach predictions
- **JPL Horizons**: Ephemeris data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality (`pytest && ruff check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use type hints for all functions
- Keep functions small and focused

## 📈 Performance

- Async/await throughout for non-blocking I/O
- Connection pooling for NASA API calls
- Efficient pandas operations for data processing
- Caching strategies for frequently accessed data

## 🔧 Configuration

### Environment Variables

```bash
# .env file
NASA_API_KEY=your_nasa_api_key
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_CONCURRENT_REQUESTS=10
```

### API Rate Limits

- **DEMO_KEY**: 30 requests per hour, 50 requests per day
- **Personal API Key**: 1000 requests per hour

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you installed in development mode
pip install -e .
```

**NASA API Rate Limits**
```bash
# Get a free API key from NASA
# https://api.nasa.gov/
```

**Type Checking Errors**
```bash
# Install type stubs
pip install types-requests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NASA for providing comprehensive asteroid data APIs
- The FastAPI team for the excellent web framework
- The Scientific Python community for amazing tools

---

## 🔮 Roadmap

- [ ] Real-time asteroid tracking
- [ ] Machine learning for impact prediction
- [ ] Advanced orbital mechanics calculations
- [ ] Interactive 3D visualization frontend
- [ ] Multi-language support for asteroid names
- [ ] Export capabilities (CSV, JSON, KML)
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

---

**Built with ❤️ for the space science community**
