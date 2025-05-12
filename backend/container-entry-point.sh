#!/bin/bash

python3 manage.py migrate

if [ -d static_backend ]; then
  rm -rf static_backend
fi

python3 manage.py collectstatic

cp -r static_backend /static
rm -rf static_backend

if [ ! -d /static/media ]; then
  mkdir -p /static/media
fi

python3 load_ingredients.py && echo "Loading load_ingredients - OK" || echo "Loading load_ingredients - ERROR"

if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 0 ] ; then
  # "DEBUG"
  python3 manage.py runserver "0:8000"
else
  # "PROD"
  gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
