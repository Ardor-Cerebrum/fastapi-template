# Core Configuration Module

This module handles application configuration, security utilities, and core constants.

## Purpose

The `app/core` module provides:
- Environment-based configuration management
- Application constants and basic utilities
- Logging setup and configuration

## Key Files

### config.py
Manages application configuration using Pydantic Settings with environment variable support.

**Expected Environment Variables:**
```bash
# Database
DATABASE_URL=

# Application
PROJECT_NAME="FastAPI Template"
VERSION="1.0.0"
DEBUG=False

# CORS
ALLOWED_HOSTS=["localhost", "127.0.0.1"]
```

### security.py
Placeholder for future security implementations. Add authentication and authorization as needed.

### constants.py
Application-wide constants and enums.

**Example Usage:**
```python
from app.core.constants import HTTPMethod, Messages

# Use HTTP method enum
if request.method == HTTPMethod.POST:
    # Handle POST request
    pass

# Use standard messages
return {"message": Messages.SUCCESS}
```

## Integration Points

- **Database**: Uses `DATABASE_URL` from settings to connect to the database
- **API**: Provides `SECRET_KEY` for JWT token signing
- **Services**: Security functions used by user service for password management
- **Main App**: Settings loaded during application startup

## Environment Setup

Create a `.env` file in the project root:
```env
DATABASE_URL=
SECRET_KEY=
PROJECT_NAME="FastAPI Template"
DEBUG=True
```

## Best Practices

1. **Never hardcode secrets** - Always use environment variables
2. **Use type hints** - Pydantic Settings provides automatic validation
3. **Validate settings** - Use Pydantic validators for complex validation logic
4. **Environment-specific configs** - Use different `.env` files for dev/staging/prod
