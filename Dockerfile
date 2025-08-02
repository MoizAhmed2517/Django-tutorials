# Use an official Python runtime as a parent image
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv

# Upgrade pip
RUN pip install --upgrade pip

# Set work directory
WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Copy project code
COPY ./src/ /code/

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DEBUG=0
ENV DEBUG=${DEBUG}

### Adding some static file command
#### Write some bash script to download local css and js files  ----> 
## But this is something which beginner developer do as django expert 
### you need to make your own python manage.py command
RUN python manage.py vendor_pull  
RUN python manage.py collectstatic --noinput

# Set project name argument with default
ARG PROJ_NAME="saas"

# Create entrypoint script to run migrations and start Gunicorn
RUN printf "#!/bin/bash\n" > ./entrypoint.sh && \
    printf "set -e\n\n" >> ./entrypoint.sh && \
    printf "echo 'Running migrations...'\n" >> ./entrypoint.sh && \
    printf "python manage.py migrate --no-input\n\n" >> ./entrypoint.sh && \
    printf "echo 'Starting Gunicorn...'\n" >> ./entrypoint.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind 0.0.0.0:\${PORT:-8000}\n" >> ./entrypoint.sh

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Expose port (optional, for documentation)
EXPOSE 8000

# Use the entrypoint script as the container's startup command
CMD ["./entrypoint.sh"]