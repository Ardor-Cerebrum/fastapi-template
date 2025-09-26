# CRUD Operations Layer

This module contains classes that handle Create, Read, Update, Delete operations directly on the database using SQLAlchemy ORM.

## Purpose

The `app/crud` module provides:
- Direct database operations (CRUD)
- Reusable database access patterns
- Type-safe database queries
- Separation of data access from business logic
- Consistent interface for database operations

## Key Files

### crud_user.py
Contains the CRUDUser class with all user-related database operations.

**Example Usage:**
```python
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate, UserUpdate
from app.db.deps import get_db

db = next(get_db())

# Create a user
user_create = UserCreate(email="test@example.com", name="Test User", password="secret")
new_user = crud_user.create(db, obj_in=user_create)

# Get a user by ID
user = crud_user.get(db, id=1)

# Get multiple users with pagination
users = crud_user.get_multi(db, skip=0, limit=10)

# Update a user
user_update = UserUpdate(name="Updated Name")
updated_user = crud_user.update(db, db_obj=user, obj_in=user_update)

# Delete a user
crud_user.remove(db, id=1)
```

### base.py
Contains a base CRUD class that can be inherited by specific CRUD classes.

**Example Usage:**
```python
from app.crud.base import CRUDBase
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

crud_user = CRUDUser(User)
```