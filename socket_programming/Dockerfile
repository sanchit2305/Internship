# # Use an official Python runtime as a parent image
# FROM python:3.8

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Define the command to run your Python script
# CMD ["python", "your_script.py"]
# Use the official Python image as the base image
FROM python:3.8

# Set the working directory within the container
WORKDIR /app

# Copy the Python script to the container
COPY receiver.py /app/

# Install any dependencies needed by your script
# You may need to modify this depending on your script's requirements
RUN pip install lz4 pylzma

# Run the Python script when the container starts
CMD ["python", "receiver.py"]