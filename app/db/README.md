# Database Layer

This module handles all database-related functionality including models, connections, and session management.

## Purpose

The `app/db` module provides:
- SQLAlchemy database engine and session management
- Database models (ORM classes)
- Database connection utilities
- Dependency injection for database sessions

## Key Files

### database.py
Contains the main database engine, session factory, and base declarative class.

### deps.py
Provides dependency injection for FastAPI routes to get database sessions.

**Example Usage:**
```python
from fastapi import Depends
from app.db.deps import get_db
from app.db.models.user import User

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### models/
Directory containing SQLAlchemy ORM models.

#### models/base.py
Base model with common fields like id, created_at, updated_at.

**Example Usage:**
```python
from app.db.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    name = Column(String)
```

#### models/user.py
Example User model demonstrating relationships and constraints.


## Database Configuration

The database connection is configured through environment variables:

```env
# PostgreSQL (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# MySQL (Alternative)
DATABASE_URL=mysql://user:password@localhost:3306/mydb
```
