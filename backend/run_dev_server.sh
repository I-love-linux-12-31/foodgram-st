#!/bin/bash

if [ -f .env ]; then
  echo "Using .env file"
  set -a
  source .env
fi

if [ -d venv ]; then
  echo "Using venv"
  source venv/bin/activate
  python3 --version
fi

python3 manage.py migrate

if [ ! -d static_backend ]; then
  python3 manage.py collectstatic
  mkdir -p static_backend/media
fi


echo "Launching load_ingredients script"
python3 load_ingredients.py && echo "Ok" || echo "ERROR"

echo "Running server..."
echo "Debug: $DEBUG"

# python3 manage.py runserver
if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 0 ] ; then
  # "DEBUG"
  python3 manage.py runserver "0:8000"
else
  # "PROD"
  gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
