#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --no-input

echo Test cache
python manage.py test_cache

echo Apply migrations
python manage.py migrate --noinput

echo Create superuser
python manage.py createsuperuser --noinput || true

exec uwsgi --ini /app/deploy/config.ini
