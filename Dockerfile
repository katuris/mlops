# Use an official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install system certificates (important for SSL verification)
RUN apt-get update && apt-get install -y ca-certificates

# Copy requirements file and install dependencies with trusted hosts
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8900

# Command to run the API
CMD ["uvicorn", "MLApp:app", "--host", "0.0.0.0", "--port", "80"]
