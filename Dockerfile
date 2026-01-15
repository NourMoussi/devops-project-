# Stage 1: Build
FROM python:3.9-slim as builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Run
FROM python:3.9-slim

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Install curl for healthcheck
# Install curl for healthcheck and upgrade pip/setuptools to fix vulnerabilities
RUN apt-get update && \
    apt-get install -y curl && \
    pip install --no-cache-dir --upgrade pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Change ownership of the application directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
