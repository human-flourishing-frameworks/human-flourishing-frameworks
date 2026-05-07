# Human Flourishing Frameworks - Docker Node
# Build: docker build -t hff-node .
# Run: docker run -p 5000:5000 hff-node

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard_app.py .
COPY ingest_api.py .
COPY governance_init.py .
COPY prediction_engine.py .
COPY healthcare_collector.py .
COPY government_collector.py .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/status || exit 1

# Run application
CMD ["python", "dashboard_app.py"]
