FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first (Docker cache optimization)
COPY backend/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./backend

# Make start script executable
RUN chmod +x backend/start.sh

# Expose port used by Gunicorn (Koyeb uses 8080)
EXPOSE 8080

# Run application
CMD ["bash", "backend/start.sh"]
