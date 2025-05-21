# Use official Python base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y chromium chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Ensure log directory exists
RUN mkdir -p logs && chmod -R 755 logs

# Command to run the application
CMD ["python", "src/main.py"]
