#!/bin/sh
# exit immediately if a command exits with a non-zero status
set -e

echo "Running Django migrations..."
uv run python3 manage.py makemigrations --noinput
uv run python3 manage.py migrate --noinput

echo "Collecting static files..."
uv run python3 manage.py collectstatic --noinput

echo "Starting Django server..."
# You can also start Gunicorn here instead of runserver
exec "$@"
