# In this Dockerfile, we use the Python 3.10 slim buster image from Docker. 
# The working directory inside the Docker container is set to /app. 
# We copy the entire application content into this /app folder inside the container.
FROM python:3.10-slim-buster
WORKDIR /app 
COPY . /app

#apt update and install awscli are useful for interacting with AWS services
RUN apt update -y && apt install awscli -y


# Install dependencies
RUN apt-get update && pip install -r requirements.txt 


# Expose port 5000 for the application, this means that the application will be accessible on this port.
CMD ["python3", "app.py"]