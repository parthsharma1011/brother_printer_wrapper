# Brother QL-700 Label Printer Web Interface
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libusb-1.0-0 \
    libusb-1.0-0-dev \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webapp/ ./webapp/
COPY scripts/ ./scripts/

# Create necessary directories
RUN mkdir -p webapp/uploads webapp/defaults

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV NO_BROWSER=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "webapp/app.py"]