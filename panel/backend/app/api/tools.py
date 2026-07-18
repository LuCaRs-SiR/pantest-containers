from fastapi import APIRouter
from app.schemas import Target, Domain, Command
from app.services import run_in_container, list_reports, get_report

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
    return run_in_container(
        "autopentestx", ["python3", "/app/main.py", "--version"]
    )


@router.post("/inspector")
def inspector(payload: Target):
    return run_in_container(
        "inspector", ["python3", "/app/core/inspector.py", "-h"]
    )


@router.post("/burp")
def burp(payload: Command):
    return run_in_container("burp", ["bash", "-lc", payload.command])


@router.post("/kali")
def kali(payload: Command):
    return run_in_container("kali-tools", ["bash", "-lc", payload.command])


@router.get("/reports")
def reports():
    return {"reports": list_reports()}


@router.get("/reports/{report_id}")
def report_details(report_id: str):
    return get_report(report_id)
