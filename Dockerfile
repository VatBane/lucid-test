# Base image
FROM python:3.12.6-slim as builder

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user
RUN useradd -m worker

# Create virtual environment
RUN python -m venv /home/worker/venv
ENV PATH="/home/worker/venv/bin:$PATH"

# Copy and install dependencies
WORKDIR /home/worker/app
COPY --chown=worker:worker requirements.txt .
RUN pip install -r requirements.txt --no-cache

# Final image
FROM python:3.12.6-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user
RUN useradd -m worker

# Copy virtual environment from builder
COPY --from=builder --chown=worker:worker /home/worker/venv /home/worker/venv
ENV PATH="/home/worker/venv/bin:$PATH"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create directory structure
WORKDIR /home/worker/app

# Copy application code
COPY --chown=worker:worker app/ /home/worker/app/
# COPY --chown=worker:worker pyproject.toml /home/worker/

# Set Python path to include the app directory
ENV PYTHONPATH="/home/worker/app:$PYTHONPATH"

# Expose ports (adjust as needed for your application)
EXPOSE 8000

# Switch to non-root user
USER worker

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]