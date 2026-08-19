FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first to leverage Docker caching
COPY requirements.txt .

# FIX: Increased timeout to 1000s and added retries to prevent download timeouts
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 -r requirements.txt

# Copy application source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Start Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]