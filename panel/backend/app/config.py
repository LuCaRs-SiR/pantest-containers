import os

AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://ai-gateway:8000")
DOCKER_SOCKET = os.getenv("DOCKER_SOCKET", "unix:///var/run/docker.sock")
