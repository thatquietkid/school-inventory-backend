# Use official Python base image
FROM python:3.13-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run init_admin.py before starting the FastAPI app
CMD ["sh", "-c", "python app/init_admin.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
