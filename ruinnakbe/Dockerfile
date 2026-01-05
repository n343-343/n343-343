# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .
COPY templates templates

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME NoakhaliAISystem

# Run main.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
