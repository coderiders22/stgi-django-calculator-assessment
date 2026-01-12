# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are shown immediately (no buffering)
ENV PYTHONUNBUFFERED=1

# Copy dependency file first (Docker layer caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into container
COPY . .

# Expose Django/Gunicorn port
EXPOSE 8000

# Start application using custom startup script
CMD ["bash", "start.sh"]
