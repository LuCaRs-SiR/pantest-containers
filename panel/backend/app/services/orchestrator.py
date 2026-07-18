from datetime import datetime, timezone
from uuid import uuid4

from app.services.docker import run_in_container
from app.services.reports import save_report


def _normalize(text: str | None) -> str:
    if not text:
        return ""
    return text.strip().lower()


def _build_plan(
    task: str,
    target: str | None,
    domain: str | None,
) -> list[dict]:
    t = _normalize(task)
    steps: list[dict] = []

    recon_keywords = [
        "recon",
        "rekones",
        "subdomen",
        "subdomain",
        "domena",
        "enumer",
    ]
    scan_keywords = ["nmap", "port", "uslug", "service", "skan", "scan"]
    inspect_keywords = ["inspector", "analiz", "raport", "triage"]
    auto_keywords = ["autopentest", "workflow", "automaty"]

    if domain and any(k in t for k in recon_keywords):
        steps.append(
            {
                "tool": "recon",
                "label": "Enumeracja domeny i subdomen",
                "container": "recon",
                "command": ["subfinder", "-d", domain],
            }
        )

    if target and any(k in t for k in scan_keywords):
        steps.append(
            {
                "tool": "nmap",
                "label": "Skan usług i portów",
                "container": "nmap-suite",
                "command": ["nmap", "-sV", target],
            }
        )

    if target and any(k in t for k in inspect_keywords):
        steps.append(
            {
                "tool": "inspector",
                "label": "Analiza wyników i inspekcja",
                "container": "inspector",
                "command": ["python3", "/app/core/inspector.py", "-h"],
            }
        )

    # For mixed tasks with both domain and host target,
    # run a standard sequence.
    if domain and target and not steps:
        steps.extend(
            [
                {
                    "tool": "recon",
                    "label": "Enumeracja domeny i subdomen",
                    "container": "recon",
                    "command": ["subfinder", "-d", domain],
                },
                {
                    "tool": "nmap",
                    "label": "Skan usług i portów",
                    "container": "nmap-suite",
                    "command": ["nmap", "-sV", target],
                },
                {
                    "tool": "inspector",
                    "label": "Analiza wyników i inspekcja",
                    "container": "inspector",
                    "command": ["python3", "/app/core/inspector.py", "-h"],
                },
            ]
        )

    if any(k in t for k in auto_keywords):
        steps.append(
            {
                "tool": "autopentestx",
                "label": "Sprawdzenie automatyzacji workflow",
                "container": "autopentestx",
                "command": ["python3", "/app/main.py", "--version"],
            }
        )

    if not steps:
        if target:
            steps.append(
                {
                    "tool": "nmap",
                    "label": "Domyślny skan usług i portów",
                    "container": "nmap-suite",
                    "command": ["nmap", "-sV", target],
                }
            )
        elif domain:
            steps.append(
                {
                    "tool": "recon",
                    "label": "Domyślna enumeracja domeny",
                    "container": "recon",
                    "command": ["subfinder", "-d", domain],
                }
            )
        else:
            steps.append(
                {
                    "tool": "hackagent",
                    "label": "Tryb doradczy asystenta",
                    "container": "hackagent",
                    "command": ["hackagent", "--help"],
                }
            )

    return steps


def _summary(steps: list[dict]) -> dict:
    total = len(steps)
    failed = len([x for x in steps if x.get("status") != "ok"])

    if failed == 0:
        status = "ok"
        conclusion = "Wszystkie kroki zakończone powodzeniem."
    elif failed < total:
        status = "partial"
        conclusion = (
            "Część kroków zakończona błędem. "
            "Sprawdź szczegóły raportu."
        )
    else:
        status = "failed"
        conclusion = (
            "Nie udało się wykonać żadnego kroku. "
            "Zweryfikuj dostępność narzędzi."
        )

    return {
        "status": status,
        "total_steps": total,
        "failed_steps": failed,
        "conclusion": conclusion,
    }


def execute_assistant_task(
    task: str,
    target: str | None,
    domain: str | None,
) -> dict:
    plan = _build_plan(task=task, target=target, domain=domain)
    steps_out: list[dict] = []

    for index, step in enumerate(plan, start=1):
        result = run_in_container(step["container"], step["command"])
        steps_out.append(
            {
                "order": index,
                "tool": step["tool"],
                "label": step["label"],
                "container": step["container"],
                "command": step["command"],
                "status": "ok" if result.get("exit_code") == 0 else "error",
                "exit_code": result.get("exit_code"),
                "output": result.get("output", ""),
            }
        )

    summary = _summary(steps_out)
    report_id = uuid4().hex
    created_at = datetime.now(timezone.utc).isoformat()

    report = {
        "id": report_id,
        "created_at": created_at,
        "task": task,
        "input": {"target": target, "domain": domain},
        "status": summary["status"],
        "summary": summary,
        "plan": [
            {
                "order": i + 1,
                "tool": step["tool"],
                "label": step["label"],
                "container": step["container"],
                "command": step["command"],
            }
            for i, step in enumerate(plan)
        ],
        "steps": steps_out,
    }

    report_meta = save_report(report_id=report_id, report=report)

    return {
        "report": report,
        "report_meta": report_meta,
    }
