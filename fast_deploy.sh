#!/bin/bash

mkdir -p footgram-st && cd footgram-st

if [ ! -f "docker-compose.yaml" ]; then
  wget https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/docs/fast-deploy-docker-compose.yaml -O docker-compose.yaml
else
  echo "docker-compose.yaml already exists!"
fi

if [ ! -f docker.env ]; then
  wget https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/docker-example.env -O docker.env
else
  echo "docker.env already exists!"
fi

echo "Files downloaded. Launching containers..."

if [ -z "$USE_PODMAN" ] || [ "$USE_PODMAN" -eq 0 ]; then
  # USE_PODMAN = 0 or not defined
  # Docker
  echo "Using docker-compose"
  sudo docker-compose up
else
  # Podman
  echo "Using podman-compose"
  podman-compose up
fi
