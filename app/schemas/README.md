# Pydantic Schemas

This module defines Pydantic models used for request/response serialization and validation in the FastAPI application.

## Purpose

The `app/schemas` module provides:
- Request/response data validation
- API documentation through schema definitions
- Type hints for better IDE support
- Data transformation between API and database layers
- Input sanitization and output formatting

## Key Files

### user.py
Defines user-related schemas for different operations.

**Example Usage:**
```python
from app.schemas.user import UserCreate, UserRead, UserUpdate

# Creating a new user (input validation)
user_data = UserCreate(
    email="user@example.com",
    name="John Doe",
    password="secure_password"
)

# Reading user data (output serialization)
user_response = UserRead(
    id=1,
    email="user@example.com",
    name="John Doe",
    is_active=True,
    created_at=datetime.utcnow()
)

# Updating user (partial input validation)
user_update = UserUpdate(name="Jane Doe")
```

### common.py
Contains reusable base schemas and mixins.

**Example Usage:**
```python
from app.schemas.common import PaginatedResponse, TimestampMixin

# Paginated response wrapper
paginated_users = PaginatedResponse[UserRead](
    items=[user1, user2, user3],
    total=100,
    page=1,
    size=10,
    pages=10
)

# Using timestamp mixin
class UserRead(TimestampMixin):
    id: int
    email: str
    name: str
    # created_at and updated_at inherited from TimestampMixin
```
