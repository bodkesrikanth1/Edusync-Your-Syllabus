FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory for SQLite (if not using MySQL)
RUN mkdir -p /tmp/data

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Copy startup script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=7860

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "4", "--worker-class", "sync", "--timeout", "120", "app:app"]
