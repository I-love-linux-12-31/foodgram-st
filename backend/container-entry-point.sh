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

# todo: use wsgi server in future
python3 manage.py runserver "0:8000"
