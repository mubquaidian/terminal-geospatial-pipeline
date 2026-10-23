# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by rasterio/GDAL
# This includes libexpat1 which was missing and causing the error
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libexpat1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the test suite automatically when the container starts
CMD ["pytest", "-v", "tests/"]