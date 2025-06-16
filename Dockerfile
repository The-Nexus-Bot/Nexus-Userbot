FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file
COPY dependencies.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p plugins logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8080

# Create a non-root user
RUN useradd -m nexususer && chown -R nexususer:nexususer /app
USER nexususer

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the application
CMD ["python", "main.py"]