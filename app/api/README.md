# API Routes Layer

This module contains FastAPI routers and route handlers that expose HTTP endpoints for the application.

## Purpose

The `app/api` module provides:
- HTTP endpoint definitions
- Request/response handling
- Route organization and grouping
- API documentation integration
- Basic dependencies like pagination

## Key Files

### routes/user.py
Contains user-related API endpoints.

**Example Usage:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.routes.user import router as user_router

# Usage in main application
app.include_router(user_router, prefix="/api/v1")

# Available endpoints:
# POST /api/v1/users/ - Create user
# GET /api/v1/users/ - List users
# GET /api/v1/users/{user_id} - Get user by ID
# PUT /api/v1/users/{user_id} - Update user
# DELETE /api/v1/users/{user_id} - Delete user
```

### api_router.py
Aggregates all route modules into a single router.

**Example Usage:**
```python
from app.api.api_router import api_router

# Include all API routes at once
app.include_router(api_router, prefix="/api/v1")
```

### deps.py
Contains API-level dependencies like pagination.

**Example Usage:**
```python
from app.api.deps import get_pagination_params
from app.db.deps import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/users/")
def list_users(
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_db)
):
    return user_service.list_users(db, pagination["skip"], pagination["limit"])
```


## Best Practices

1. **Use dependency injection**: Leverage FastAPI's dependency system
2. **Proper status codes**: Use appropriate HTTP status codes
3. **Error handling**: Provide meaningful error messages
4. **Documentation**: Add docstrings and OpenAPI metadata
5. **Validation**: Use Pydantic models for request/response validation
