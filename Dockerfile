ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

## set some environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

### Installing system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    $$ rm -rf /var/lib/apt/lists/*

## Create and activate a virtual environment
RUN python -m venv /opt/venv

## Upgrade pip
RUN pip install --upgrade pip

## set workdir
RUN /code

## Copy requirements first for better caching
COPY requirements.txt /tmp/requirements.txt

## Install requirements
RUN pip install --no-cache-dir -r /tmp/requirements.txt

## COPY project code
COPY ./src/ /code/

## Set project name
ARG PROJ_NAME="saas"

## Start Gunicorn server and creating entrypoint script
RUN printf "#!/bin/bash\n" > ./entrypoint.sh && \
    printf "set -e\n\n" >> ./entrypoint.sh && \
    printf "echo 'Running migration...'\n" >> ./entrypoint.sh && \
    printf "python manage.py migrate --no-input\n\n" >> ./entrypoint.sh && \
    printf "echo 'starting gunicorn... '\n" >> ./entrypoint.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind 0.0.0.0:\${PORT:-8000}\n" >> ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]