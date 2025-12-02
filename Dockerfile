# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies (disable pip progress bar to avoid threading issues)
RUN pip install --no-cache-dir --disable-pip-version-check --no-input -r requirements.txt

# Copy entire project into container
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run Flask app on port 5000
CMD ["python", "app.py"]
