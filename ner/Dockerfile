# Use a more complete ARM-compatible base image for Python
FROM arm64v8/python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed by spaCy and other libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install the spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the application code to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "engine.py"]