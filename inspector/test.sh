#!/usr/bin/env bash
set -euo pipefail

if [ -z "${DOCKER_API_VERSION+x}" ]; then
  export DOCKER_API_VERSION=1.44
fi

cd "$(dirname "$0")"/..

echo "Building inspector..."
env DOCKER_API_VERSION="$DOCKER_API_VERSION" docker compose build inspector

echo "Starting inspector..."
env DOCKER_API_VERSION="$DOCKER_API_VERSION" docker compose up -d inspector
sleep 2

echo "Checking inspector container status..."
container_status=$(docker ps --filter name=inspector --format '{{.Status}}')
if [ -z "$container_status" ]; then
  echo "ERROR: inspector container is not running"
  exit 1
fi

echo "Running smoke test..."
docker exec inspector python3 /app/core/inspector.py -h | head -n 5

echo "Inspector smoke test passed."
