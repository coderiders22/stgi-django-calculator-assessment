# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory to backend folder
WORKDIR /app/backend

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1

# Copy backend requirements first (better Docker cache)
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Expose port (Gunicorn will bind dynamically)
EXPOSE 8080

# Run startup script (migrations + collectstatic + gunicorn)
CMD ["bash", "start.sh"]
