# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# The GUI tester requires Tkinter which is usually in the base image, 
# but we'll ensure it's there if needed for other Linux distros.
# However, for the judge, we don't need GUI libs.
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Create the submissions directory if it doesn't exist
RUN mkdir -p submissions

# Run judge.py when the container launches
CMD ["python", "judge.py"]
