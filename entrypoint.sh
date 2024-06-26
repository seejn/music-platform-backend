#!/bin/sh

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 backend.wsgi:application