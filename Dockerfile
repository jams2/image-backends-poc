FROM python:3.11.4-slim-bookworm

# Add user that will be used in the container.
ARG HOSTUID=1000
RUN useradd wagtail --uid=${HOSTUID} && mkdir /home/wagtail && chown -R wagtail:wagtail /home/wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN chown -R wagtail:wagtail /app

USER wagtail
COPY --chown=wagtail:wagtail ./ ./
RUN python -m pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=image_backends.settings.dev
CMD set -xe; \
    python manage.py migrate --noinput; \
    python manage.py collectstatic --noinput --clear; \
    python manage.py runserver 0.0.0.0:8000
