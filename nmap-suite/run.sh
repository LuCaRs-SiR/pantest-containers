#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="pantest-nmap-suite"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

usage() {
  cat <<EOF
Usage: $0 <command> [args]

Commands:
  build           Build the nmap-suite Docker image
  shell           Start an interactive bash shell in the nmap-suite container
  test            Verify the container and nmap installation
  scan <target>   Run nmap against the given target

Example:
  $0 build
  $0 shell
  $0 test
  $0 scan 127.0.0.1
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

case "$1" in
  build)
    docker build -t "$IMAGE_NAME" .
    ;;
  shell)
    docker run --rm -it --network host "$IMAGE_NAME" bash
    ;;
  test)
    docker run --rm --network host "$IMAGE_NAME" nmap --version
    echo '---'
    docker run --rm --network host "$IMAGE_NAME" nmap -sn 127.0.0.1
    ;;
  scan)
    shift
    if [[ $# -lt 1 ]]; then
      echo "Usage: $0 scan <target>"
      exit 1
    fi
    docker run --rm --network host "$IMAGE_NAME" nmap "$@"
    ;;
  *)
    usage
    exit 1
    ;;
esac
