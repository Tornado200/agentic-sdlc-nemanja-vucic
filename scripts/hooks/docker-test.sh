#!/usr/bin/env bash
# Builds the Docker image and runs the tests inside it.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
    echo "docker not found, skipping Docker tests"
    exit 0
fi

docker build -q -t kata-tests . >/dev/null
docker run --rm kata-tests
