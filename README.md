# FastAPI Template

A modern, production-ready FastAPI template with a clean architecture, comprehensive testing setup, and best practices.

## 🚀 Features

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Powerful ORM with type hints support
- **Pydantic**: Data validation using Python type annotations
- **Code Quality**: Pre-configured with Black and isort
- **Database**: SQLite for development, easy to switch to PostgreSQL
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Clean Architecture**: Simple layered architecture

## 📁 Project Structure

```
fastapi-template/
├── app/                    # Application code
│   ├── api/                # API layer
│   │   ├── routes/         # API route handlers
│   │   └── README.md       # API documentation
│   ├── core/               # Core configuration
│   │   └── README.md       # Core module documentation
│   ├── crud/               # Database CRUD operations
│   │   └── README.md       # CRUD documentation
│   ├── db/                 # Database layer
│   │   ├── models/         # SQLAlchemy models
│   │   └── README.md       # Database documentation
│   ├── schemas/            # Pydantic schemas
│   │   └── README.md       # Schema documentation
│   └── services/           # Business logic layer
│       └── README.md       # Services documentation
├── scripts/                # Utility scripts
│   └── README.md           # Scripts documentation
├── tests/                  # Test files
│   └── README.md           # Testing documentation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── pytest.ini            # Pytest configuration
└── README.md              # This file
```

## 🛠️ Quick Start

### Prerequisites

- Python 3.12+
- pip or pipenv


## 🏗️ Architecture

This template follows a layered architecture pattern:

```
┌─────────────────┐
│   API Layer     │  ← FastAPI routes, request/response handling
├─────────────────┤
│ Services Layer  │  ← Business logic, external API calls
├─────────────────┤
│   CRUD Layer    │  ← Database operations, data access
├─────────────────┤
│ Database Layer  │  ← SQLAlchemy models, database connection
└─────────────────┘
```

### Layer Responsibilities

- **API Layer** (`app/api/`): HTTP endpoints, request validation, response formatting
- **Services Layer** (`app/services/`): Business logic, workflow orchestration
- **CRUD Layer** (`app/crud/`): Database operations, data access patterns
- **Database Layer** (`app/db/`): Models, database configuration, connections
- **Schemas** (`app/schemas/`): Data validation, serialization models
- **Core** (`app/core/`): Configuration, security, constants


### Database Configuration

**PostgreSQL (Production)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

**MySQL**
```env
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

## 🧩 Module Documentation

Each module has detailed documentation in its respective README.md file:

## 🚀 Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
