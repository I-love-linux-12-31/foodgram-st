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

python3 manage.py runserver
