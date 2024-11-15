# Use the official Python image
FROM python:3.11-slim

# Set environment variables to avoid issues with interactive prompts during the install process
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set a working directory for the application
WORKDIR /app

# Copy the application files and requirement
COPY main.py test.py testData.py loginInfo.py apiTest.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "python-jose[cryptography]==3.3.0"


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 8000



# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# Create image: docker build -t fastapi-app .
# Run the docker container: docker run -d -p 8000:8000 fastapi-app
# Run test
    # pytest test.py
    # pytest apiTest.py