import os
import requests
import docker
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Pantest Panel Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://ai-gateway:8000")
CONTAINER_SOCKET = os.getenv("DOCKER_SOCKET", "unix:///var/run/docker.sock")

docker_client = docker.DockerClient(base_url=CONTAINER_SOCKET)


class Target(BaseModel):
    target: str


class Domain(BaseModel):
    domain: str


class Prompt(BaseModel):
    model: str = "qwen2.5:14b-instruct"
    prompt: str


def proxy_ai(payload: dict) -> dict:
    try:
        r = requests.post(
            f"{AI_GATEWAY_URL}/api/generate",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))


def run_in_container(name: str, command: list[str]) -> dict:
    try:
        container = docker_client.containers.get(name)
        result = container.exec_run(command, tty=False, demux=False)
        output = result.output.decode("utf-8", errors="replace") if result.output else ""
        return {"output": output, "exit_code": result.exit_code}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/status")
def status():
    try:
        r = requests.get(f"{AI_GATEWAY_URL}/health", timeout=5)
        ai_status = r.json()
    except Exception as exc:
        ai_status = {"error": str(exc)}
    return {"ai_gateway": ai_status, "backend": "ok"}


@app.post("/api/ai")
def ai_chat(payload: Prompt):
    return proxy_ai(payload.model_dump())


@app.post("/api/nmap")
def nmap_scan(payload: Target):
    return run_in_container("nmap-suite", ["nmap", "-sV", payload.target])


@app.post("/api/recon")
def recon_scan(payload: Domain):
    return run_in_container("recon", ["subfinder", "-d", payload.domain])


@app.post("/api/hackagent")
def hackagent(payload: Target):
    return run_in_container("hackagent", ["hackagent", "--help"])


@app.post("/api/autopentestx")
def autopentestx(payload: Target):
    return run_in_container("autopentestx", ["python3", "/app/main.py", "--version"])


@app.post("/api/inspector")
def inspector(payload: Target):
    return run_in_container("inspector", ["python3", "/app/core/inspector.py", "-h"])


@app.get("/api/reports")
def reports():
    return {"reports": []}
