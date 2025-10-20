FROM python:3.12-slim

WORKDIR /app

# Define ARG and ENV for port
ARG ARDOR_PORT=1337
ENV ARDOR_PORT=${ARDOR_PORT}

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose configurable port
EXPOSE ${ARDOR_PORT}

# Start uvicorn with configured port
CMD uvicorn main:app --host 0.0.0.0 --port ${ARDOR_PORT}
