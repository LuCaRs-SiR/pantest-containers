#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="pantest-kali-tools"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

usage() {
  cat <<EOF
Usage: $0 <command> [args]

Commands:
  build           Build the kali-tools Docker image
  shell           Start an interactive bash shell in the kali container
  test            Verify the container and Kali tools installation
  scan <target>   Example command: run nmap or other tool against target

Example:
  $0 build
  $0 shell
  $0 test
  $0 scan 192.168.1.1
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
    docker run --rm -it --network host -v "$SCRIPT_DIR":/tools "$IMAGE_NAME" bash
    ;;
  test)
    docker run --rm --network host -v "$SCRIPT_DIR":/tools "$IMAGE_NAME" bash -lc "nmap --version && echo '---' && sqlmap --help | head -n 5"
    ;;
  scan)
    shift
    if [[ $# -lt 1 ]]; then
      echo "Usage: $0 scan <target>"
      exit 1
    fi
    docker run --rm --network host -v "$SCRIPT_DIR":/tools "$IMAGE_NAME" nmap "$@"
    ;;
  *)
    usage
    exit 1
    ;;
esac
