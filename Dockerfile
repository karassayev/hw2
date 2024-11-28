# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN pip install elasticsearch

# Run application
CMD ["python", "task3.py"]
