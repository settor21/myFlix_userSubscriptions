# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Gunicorn
RUN pip install gunicorn

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Run app.py when the container launches
# CMD ["python", "app.py"]
# Run Gunicorn when the container launches in production
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]

