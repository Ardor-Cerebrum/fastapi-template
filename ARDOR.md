# Ardor FastAPI Template - Developer Agent Guide

## Project Overview

This template is a modern, production-ready FastAPI application with clean architecture built on separation of concerns principles. The project follows a multi-layered architecture with clear separation between API, business logic, data, and configuration.

### Key Features

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy 2.0**: ORM with full type support
- **Pydantic v2**: Data validation using Python type annotations
- **Clean Architecture**: Multi-layered structure with separation of concerns
- **uv**: Fast Python package manager for dependency management
- **Docker**: Containerization for easy deployment
- **Code Quality**: Configured Black, isort, Ruff linter, and pre-commit hooks

## Project Architecture

The project follows a multi-layered architecture:

```
┌─────────────────┐
│   API Layer     │  ← FastAPI routers, request/response handling
├─────────────────┤
│ Services Layer  │  ← Business logic, external API calls
├─────────────────┤
│   CRUD Layer    │  ← Database operations, data access
├─────────────────┤
│ Database Layer  │  ← SQLAlchemy models, database connection
└─────────────────┘
```

### Folder Structure

```
fastapi-template/
├── main.py                    # FastAPI application entry point
├── pyproject.toml            # Project metadata and dependencies (uv)
├── uv.lock                   # Dependency lock file
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── .python-version           # Python version specification for uv
├── Dockerfile               # Docker configuration
├── app/                     # Main application code
│   ├── api/                 # API layer - HTTP endpoints
│   │   ├── deps.py         # API dependencies (pagination)
│   │   └── README.md       # API layer documentation
│   ├── core/                # Core - configuration and utilities
│   │   ├── config.py       # Application settings (Pydantic Settings)
│   │   ├── constants.py    # Constants and enums
│   │   ├── security.py     # Security (placeholder)
│   │   ├── utils.py        # Utilities (logging)
│   │   └── README.md       # Core documentation
│   ├── crud/                # CRUD operations
│   │   ├── base.py         # Base CRUD class with typing
│   │   └── README.md       # CRUD documentation
│   ├── db/                  # Database
│   │   ├── database.py     # DB connection, sessions
│   │   ├── deps.py         # DB dependencies for DI
│   │   ├── models/         # SQLAlchemy models
│   │   │   └── base.py     # Base model
│   │   └── README.md       # DB documentation
│   ├── schemas/             # Pydantic schemas
│   │   ├── common.py       # Common base schemas
│   │   └── README.md       # Schemas documentation
│   └── services/            # Business logic
│       └── README.md       # Services documentation
└── README.md               # General project documentation
```

## Detailed Layer Guide

### 1. Database Layer (`app/db/`)

#### database.py
- **Purpose**: SQLAlchemy engine setup, sessions, and base model
- **Key Components**:
  - `engine`: SQLAlchemy engine (different settings for SQLite/PostgreSQL)
  - `SessionLocal`: Session factory
  - `Base`: Base class for declarative models
  - `get_db()`: Session generator for FastAPI dependencies
  - `create_tables()`: Create all database tables

#### deps.py
- **Purpose**: Dependencies for database injection into FastAPI routes
- **Key Functions**:
  - `get_db()`: Main dependency for getting DB session
  - `get_db_session()`: Direct session retrieval (requires manual closing)

#### models/base.py
- **Purpose**: Base model with common fields
- **Features**:
  - Automatic table name generation from class name (CamelCase → snake_case)
  - Abstract class (`__abstract__ = True`)

### 2. CRUD Layer (`app/crud/`)

#### base.py
- **Purpose**: Generic CRUD class with typing
- **Type Variables**:
  - `ModelType`: SQLAlchemy model
  - `CreateSchemaType`: Pydantic schema for creation
  - `UpdateSchemaType`: Pydantic schema for updates

#### Main CRUD Methods
- `get()`: Get record by ID
- `get_multi()`: Get multiple records with pagination and filters
- `create()`: Create new record
- `update()`: Update existing record
- `remove()`: Delete record by ID
- `exists()`: Check record existence
- `count()`: Count records with filters
- `search()`: Search by text fields
- `bulk_create/update/delete()`: Bulk operations

### 3. Schemas Layer (`app/schemas/`)

#### common.py
- **Purpose**: Common base Pydantic schemas
- **BaseSchema**: Base configuration with `from_attributes = True`

#### Schema Structure
For each entity, typically created:
- `EntityCreate`: For creation (without ID, with required fields)
- `EntityUpdate`: For updates (all fields optional)
- `EntityRead`: For reading (with ID and computed fields)
- `EntityBase`: Common fields

### 4. Services Layer (`app/services/`)

#### Purpose
- Business logic implementation
- Coordination between CRUD operations
- External API integrations
- Complex data transformations
- Transaction management across multiple entities

#### Patterns
- One service per domain entity
- Service methods return Pydantic schemas (not DB models)
- Business rules and validations handling
- Logging and notifications

### 5. API Layer (`app/api/`)

#### deps.py
- **Purpose**: API-level dependencies
- **get_pagination_params()**: Pagination parameters from query parameters

#### Router Structure
- Each domain has its own router
- Routers are grouped in `api_router.py`
- Dependency injection usage

### 6. Core Layer (`app/core/`)

#### config.py
- **Purpose**: Application configuration via Pydantic Settings
- **Key Settings**:
  - `DATABASE_URL`: Database URL
  - `PROJECT_NAME`, `VERSION`: Application metadata
  - `DEBUG`: Debug mode
  - CORS settings
  - API prefixes

#### constants.py
- **Purpose**: Constants and enums
- **Environment**: DEVELOPMENT/PRODUCTION
- **HTTPMethod**: GET/POST/PUT/PATCH/DELETE

#### security.py
- **Purpose**: Security functions (placeholder currently)
- **Future Functions**: Password hashing, JWT tokens, authentication

#### utils.py
- **Purpose**: Common utilities
- **setup_logging()**: Logging setup

## Conventions and Best Practices

### 1. Naming

#### Files and Classes
- Models: `models/user.py` → `class User(BaseModel)`
- CRUD: `crud/crud_user.py` → `class CRUDUser(CRUDBase[User, UserCreate, UserUpdate])`
- Schemas: `schemas/user.py` → `UserCreate`, `UserRead`, `UserUpdate`
- Services: `services/user_service.py` → `class UserService`
- API: `api/routes/user.py` → `router = APIRouter()`

#### Variables
- `db`: SQLAlchemy session
- `crud_user`: CRUD class instance
- `user_service`: Service instance
- `current_user`: Current authenticated user

### 2. Type Hints

#### Using Type Hints
```python
from typing import Optional, List
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()
```

#### Generic Types in CRUD
```python
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # ...
```

### 3. Error Handling

#### In API Routes
```python
from fastapi import HTTPException, status

@app.post("/users/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### In Services
```python
class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> UserRead:
        # Business validations
        if crud_user.get_by_email(db, email=user_create.email):
            raise ValueError("Email already registered")

        # Creation
        db_user = crud_user.create(db, obj_in=user_create)
        return UserRead.from_orm(db_user)
```

### 4. Dependencies (Dependency Injection)

#### Basic Dependencies
```python
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users/")
def read_users(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
):
    return user_service.get_users(db, **pagination)
```

#### Custom Dependencies
```python
from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### 5. Pagination

#### Standard Pagination
```python
# In API deps.py
def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return")
) -> dict:
    return {"skip": skip, "limit": limit}

# In CRUD base.py
def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, **filters):
    return db.query(self.model).filter_by(**filters).offset(skip).limit(limit).all()
```

### 6. Data Validation

#### Pydantic Schemas
```python
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

### 7. Database Operations

#### SQLAlchemy Models
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### Relationships
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(String, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    author = relationship("User", back_populates="posts")

# In User model
class User(BaseModel):
    # ...
    posts = relationship("Post", back_populates="author")
```

### 8. Configuration and Environment Variables

#### .env File
```env
# Database
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application
PROJECT_NAME="FastAPI Template"
VERSION="1.0.0"
DEBUG=True
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-here

# CORS
ALLOWED_HOSTS=["localhost", "127.0.0.1"]
ALLOW_ORIGINS=["http://localhost:3000", "http://localhost:8080", "https://.*\\.ardor\\.cloud"]

# API
API_V1_STR=/api/v1
```

#### Usage in config.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = ""
    project_name: str = "FastAPI Template"
    debug: bool = False
    secret_key: str = "default-secret-key"

    class Config:
        env_file = ".env"
        case_sensitive = True
```

## New Feature Development Process

### 1. Adding New Entity

#### Step 1: Create DB Model
```python
# app/db/models/item.py
from sqlalchemy import Column, String, Float
from app.db.models.base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
```

#### Step 2: Create Pydantic Schemas
```python
# app/schemas/item.py
from pydantic import BaseModel
from app.schemas.common import BaseSchema

class ItemBase(BaseSchema):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: str | None = None
    price: float | None = None

class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

#### Step 3: Create CRUD Class
```python
# app/crud/crud_item.py
from app.crud.base import CRUDBase
from app.db.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

crud_item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
```

#### Step 4: Create Service
```python
# app/services/item_service.py
from sqlalchemy.orm import Session
from app.crud.crud_item import crud_item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

class ItemService:
    def create_item(self, db: Session, item_create: ItemCreate) -> ItemRead:
        db_item = crud_item.create(db, obj_in=item_create)
        return ItemRead.from_orm(db_item)

    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> list[ItemRead]:
        items = crud_item.get_multi(db, skip=skip, limit=limit)
        return [ItemRead.from_orm(item) for item in items]

item_service = ItemService()
```

#### Step 5: Create API Routes
```python
# app/api/routes/item.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_pagination_params
from app.db.deps import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import item_service

router = APIRouter()

@router.post("/", response_model=ItemRead)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(db, item_in)

@router.get("/", response_model=list[ItemRead])
def read_items(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
):
    return item_service.get_items(db, **pagination)
```

#### Step 6: Register Routes
```python
# app/api/api_router.py (create if doesn't exist)
from fastapi import APIRouter
from app.api.routes.item import router as item_router

api_router = APIRouter()
api_router.include_router(item_router, prefix="/items", tags=["items"])
```

#### Step 7: Connect to Main Application
```python
# main.py
from app.api.api_router import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)
```

### 2. Adding Authentication

#### Step 1: Extend User Model
```python
# app/db/models/user.py
class User(BaseModel):
    # ... existing fields
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

#### Step 2: Implement Security Functions
```python
# app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

#### Step 3: Add Authentication to API
```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.security import verify_password
from app.crud.crud_user import crud_user

def authenticate_user(db: Session, email: str, password: str):
    user = crud_user.get_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud_user.get_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

### 3. Adding Tests

#### Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── test_api/           # API tests
├── test_crud/          # CRUD tests
├── test_services/      # Service tests
└── test_db/           # DB tests
```

#### Test Example
```python
# tests/test_api/test_items.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_item(client: TestClient, db: Session):
    item_data = {"name": "Test Item", "price": 10.99}
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert "id" in data
```

## Monitoring and Logging

### Logging
```python
# app/core/utils.py
import logging

def setup_logging():
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logging()
```

### Monitoring Middleware
```python
# main.py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
    )
    return response
```

## Security

### Key Measures
1. **Input Validation**: Always use Pydantic schemas
2. **SQL Injection Protection**: Use SQLAlchemy ORM
3. **CORS**: Configure properly for production
4. **Rate Limiting**: Add request limits
5. **HTTPS**: Use in production
6. **Secrets**: Never commit to Git

### CORS Configuration
```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Performance

### Database Optimizations
1. **Indexes**: Add to frequently used fields
2. **Pagination**: Always limit result count
3. **N+1 Problem**: Use `joinedload` or `selectinload`
4. **Connection Pooling**: Configured in database.py

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_data():
    # Expensive computations or queries
    pass
```
## Development Setup and Quality Tools

### Package Management with uv

This project uses **uv** - a fast Python package manager written in Rust. It's significantly faster than pip and provides better dependency resolution.

#### Installation

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Basic Commands

```bash
# Install all dependencies (creates .venv automatically)
uv sync

# Install with development dependencies
uv sync --extra dev

# Add a new production dependency
uv add fastapi

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove package-name

# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package fastapi

# Run a command in the virtual environment
uv run uvicorn main:app --reload

# Run Python scripts
uv run python script.py

# Run tests
uv run pytest
```

#### Custom Virtual Environment Path

By default, uv creates `.venv` in the project directory. To use a custom path:

```bash
# Set via environment variable
export UV_PROJECT_ENVIRONMENT=/opt/.venv
uv sync

# Or set in .env file
echo "UV_PROJECT_ENVIRONMENT=/opt/.venv" >> .env
```

**Note**: The custom path must be absolute. For production deployments, ensure the directory exists and has proper permissions.

#### Key Benefits

- **Speed**: 10-100x faster than pip
- **Automatic venv**: Creates and manages `.venv` automatically
- **Lock file**: `uv.lock` ensures reproducible installs
- **No activation needed**: Use `uv run` instead of activating venv
- **Better resolution**: Handles complex dependency conflicts

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. The configuration includes:

- **Ruff**: Fast Python linter and formatter
- **Black**: Code formatter
- **isort**: Import sorter
- **General checks**: Trailing whitespace, end-of-file fixes, YAML validation, etc.

#### Running Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run all hooks with auto-fix
uv run pre-commit run -a --fix
```

#### Manual Code Quality Checks

```bash
# Run Ruff linter
uv run ruff check .

# Run Ruff linter with auto-fix
uv run ruff check . --fix

# Run Ruff formatter
uv run ruff format .

# Run Black formatter
uv run black .

# Run isort
uv run isort .
```

### Development Workflow

1. **Setup**: Run `uv sync --extra dev` to install all dependencies
2. **Development**: Write code following the established patterns
3. **Add dependencies**: Use `uv add` instead of manually editing pyproject.toml
4. **Quality**: Run `uv run pre-commit run -a --fix` before committing
5. **Testing**: Run `uv run pytest` to ensure all tests pass
6. **Run app**: Use `uv run uvicorn main:app --reload` for development

## Conclusion

This template provides a solid foundation for building scalable FastAPI applications. Following the described conventions and patterns, an AI agent can effectively extend and modify the project, adding new features, improving performance, and maintaining the codebase.

Key principles:
- **Separation of concerns** between layers
- **Type hints** for code reliability
- **Testability** through dependency injection
- **Extensibility** through inheritance and composition
- **Documentation** through README files and docstrings

Always follow these principles during development to maintain code quality and consistency.
