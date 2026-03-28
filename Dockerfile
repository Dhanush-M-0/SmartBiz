FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create reports output directory
RUN mkdir -p reports_output

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_ENV=production
ENV FLASK_APP=wsgi:app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run Gunicorn
CMD ["gunicorn", "--workers", "4", "--worker-class", "sync", "--timeout", "120", "--bind", "0.0.0.0:5000", "wsgi:app"]
