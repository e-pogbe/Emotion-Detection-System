# Stage 1: Builder (install dependencies)
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (slim image for production)
FROM python:3.12-slim

WORKDIR /app

# Install any system dependencies required for Gunicorn (optional)
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy built deps and source code from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

# Debugging step: Check if Gunicorn is installed (remove later if not needed)
RUN which gunicorn

# Expose port (Back4App defaults to 8080 for HTTP; match your app)
EXPOSE 8080

# Run with Gunicorn (production-ready; binds to 0.0.0.0 for container access)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api.index:app"]