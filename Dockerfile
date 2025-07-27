# Use Python 3.9 slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY test.py .
COPY main.py .

# Make main.py executable
RUN chmod +x main.py

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set the entry point
ENTRYPOINT ["python", "main.py"] 