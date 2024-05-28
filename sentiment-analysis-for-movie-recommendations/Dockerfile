# An official Python runtime as a parent image
FROM python:3.11-slim

# Setting the working directory to sentiment-analysis for movie recommendations directory
WORKDIR /app

# Copying the application code into the container dir
COPY . /app/

# Installing Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5001

CMD ["python", "main.py"]

#docker run -p 5001:5001 movieapp

