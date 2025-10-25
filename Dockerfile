# Use a supported, lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (if your app uses it)
EXPOSE 5000

# Command to run the application
CMD ["python3", "app.py"]