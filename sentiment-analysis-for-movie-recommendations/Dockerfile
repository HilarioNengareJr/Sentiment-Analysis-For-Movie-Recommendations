# Use the official Python image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the application code into the container directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001
EXPOSE 5001

# Command to run the application
CMD ["python", "main.py"]
