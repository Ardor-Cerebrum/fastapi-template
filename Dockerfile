FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Define ARG and ENV for port
ARG PORT=1337
ENV PORT=${PORT}

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose configurable port
EXPOSE ${PORT}

# Start uvicorn with configured port
CMD uv run uvicorn main:app --host 0.0.0.0 --port ${PORT}
