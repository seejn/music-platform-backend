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

RUN python manage.py makemigrations Roles
RUN python manage.py makemigrations genre
RUN python manage.py makemigrations Cusers
RUN python manage.py makemigrations track
RUN python manage.py makemigrations album
RUN python manage.py makemigrations tour
RUN python manage.py makemigrations report_ban
RUN python manage.py makemigrations


RUN python manage.py migrate Roles
RUN python manage.py migrate genre
RUN python manage.py migrate Cusers
RUN python manage.py migrate track
RUN python manage.py migrate album
RUN python manage.py migrate tour
RUN python manage.py migrate report_ban
RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
