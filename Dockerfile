FROM python:3.12-slim-bookworm

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.5 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

RUN python manage.py loaddata seed/roles.json 
RUN python manage.py loaddata seed/genres.json 
RUN python manage.py loaddata seed/users.json 
RUN python manage.py loaddata seed/tracks.json 
RUN python manage.py loaddata seed/albums.json 

RUN python manage.py collectstatic --noinput

EXPOSE 8000