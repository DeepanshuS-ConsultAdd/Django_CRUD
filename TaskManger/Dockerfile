
FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# # Use an official Python runtime as a parent image
# FROM python:3.10-slim

# # Set the working directory in the container
# WORKDIR /code

# # Copy the requirements file into the container
# COPY requirements.txt /code/

# # Install any dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container at /code
# COPY . /code/