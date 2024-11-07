# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variables to run Flask
ENV FLASK_APP=__init__.py
ENV FLASK_ENV=development

# Run the command to start the app with Gunicorn, specifying the module and factory function
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "__init__:create_app()"]
