from fastapi import APIRouter
from app.schemas import Target, Domain
from app.services import run_in_container

router = APIRouter(prefix="/api", tags=["tools"])


@router.post("/nmap")
def nmap_scan(payload: Target):
    return run_in_container("nmap-suite", ["nmap", "-sV", payload.target])


@router.post("/recon")
def recon_scan(payload: Domain):
    return run_in_container("recon", ["subfinder", "-d", payload.domain])


@router.post("/hackagent")
def hackagent(payload: Target):
    return run_in_container("hackagent", ["hackagent", "--help"])


@router.post("/autopentestx")
def autopentestx(payload: Target):
    return run_in_container("autopentestx", ["python3", "/app/main.py", "--version"])


@router.post("/inspector")
def inspector(payload: Target):
    return run_in_container("inspector", ["python3", "/app/core/inspector.py", "-h"])


@router.get("/reports")
def reports():
    return {"reports": []}
