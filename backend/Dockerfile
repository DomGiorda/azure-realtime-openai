FROM python:3.12-slim AS builder

# Set working directory for the build stage
WORKDIR /build

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Start a new stage for the runtime
FROM python:3.12-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8765

HEALTHCHECK CMD curl --fail http://localhost:8765/health || exit 1

# Run the application
CMD ["python3", "-m", "gunicorn", "app:create_app", "-b", "0.0.0.0:8765", "--worker-class", "aiohttp.GunicornWebWorker"]