# Services Layer

This module contains business logic and orchestrates operations between different layers of the application.

## Purpose

The `app/services` module provides:
- Business logic implementation
- Coordination between CRUD operations
- External API integration
- Complex data transformations
- Cross-cutting concerns (caching, logging, notifications)
- Transaction management across multiple entities

## Key Files

**Example Usage:**
```python
from app.services.base_service import BaseService

class UserService():
    def create_user(self, db: Session, user_create: UserCreate) -> UserRead:
        # Business logic here
        pass
```

## Service Pattern

### Business Logic Orchestration

Services orchestrate business operations that may involve multiple CRUD operations:

```python
from app.crud.crud_user import crud_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> UserRead:
        # 1. Validate business rules
        existing_user = crud_user.get_by_email(db, email=user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # 2. Transform data (hash password)
        hashed_password = get_password_hash(user_create.password)
        user_create.password = hashed_password

        # 3. Create user via CRUD
        db_user = crud_user.create(db, obj_in=user_create)

        # 4. Additional business logic (send welcome email, create profile, etc.)
        self._send_welcome_email(db_user.email)
        self._create_user_profile(db, db_user.id)

        # 5. Return response schema
        return UserRead.from_orm(db_user)

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[UserRead]:
        user = crud_user.get_by_email(db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise ValueError("User account is deactivated")
        return UserRead.from_orm(user)

    def create_access_token_for_user(self, user: UserRead) -> str:
        token_data = {"sub": user.email, "user_id": user.id}
        return create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
```
