# Use a lightweight Python image (Standard for Terminal Bench tasks)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the test suite automatically when the container starts
CMD ["pytest", "-v", "tests/"]