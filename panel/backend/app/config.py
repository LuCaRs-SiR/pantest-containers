import os

AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://ai-gateway:8000")
DOCKER_SOCKET = os.getenv("DOCKER_SOCKET", "unix:///var/run/docker.sock")
REPORTS_DIR = os.getenv("REPORTS_DIR", "/logs/assistant-reports")
DEFAULT_TOOL_CONTAINERS = "nmap-suite,recon,hackagent,autopentestx,inspector,"
DEFAULT_TOOL_CONTAINERS += "burp,kali-tools,ai-gateway"
RAW_TOOL_CONTAINERS = os.getenv("TOOL_CONTAINERS", DEFAULT_TOOL_CONTAINERS)
TOOL_CONTAINER_ITEMS = RAW_TOOL_CONTAINERS.split(",")
TOOL_CONTAINERS = [x.strip() for x in TOOL_CONTAINER_ITEMS if x.strip()]
