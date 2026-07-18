from datetime import datetime, timezone
import re
from uuid import uuid4

from app.services.docker import run_in_container
from app.services.reports import save_report


def _normalize(text: str | None) -> str:
    if not text:
        return ""
    return text.strip().lower()


def _extract_domain(text: str) -> str | None:
    match = re.search(r"\b([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)\b", text)
    if not match:
        return None
    value = match.group(1).strip().lower()
    if "/" in value:
        return None
    return value


def _extract_target(text: str) -> str | None:
    ipv4 = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    if ipv4:
        return ipv4.group(0)

    host_like = re.search(r"\b[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+\b", text)
    if host_like:
        return host_like.group(0).lower()

    return None


def _detect_profiles(task: str) -> list[str]:
    t = _normalize(task)

    profile_keywords = {
        "web": [
            "web",
            "http",
            "https",
            "burp",
            "xss",
            "sqli",
            "sql injection",
            "csrf",
            "cookie",
            "header",
        ],
        "api": [
            "api",
            "rest",
            "graphql",
            "swagger",
            "openapi",
            "endpoint",
        ],
        "infra": [
            "infra",
            "infrastr",
            "siec",
            "network",
            "host",
            "port",
            "service",
            "ssh",
            "rdp",
            "nmap",
            "skan",
            "scan",
        ],
        "ad": [
            "active directory",
            "ad",
            "domain controller",
            "dc",
            "kerberos",
            "ldap",
            "smb",
        ],
        "automation": ["autopentest", "workflow", "automaty", "pipeline"],
    }

    profiles: list[str] = []
    for profile, keywords in profile_keywords.items():
        if any(keyword in t for keyword in keywords):
            profiles.append(profile)

    return profiles


def _append_step(steps: list[dict], step: dict) -> None:
    marker = (step["tool"], tuple(step["command"]))
    for existing in steps:
        other = (existing["tool"], tuple(existing["command"]))
        if marker == other:
            return
    steps.append(step)


def _resolve_planner_context(
    task: str,
    target: str | None,
    domain: str | None,
) -> dict:
    resolved_domain = domain or _extract_domain(task)
    resolved_target = target or _extract_target(task)

    profiles = _detect_profiles(task)
    if not profiles:
        if resolved_domain and resolved_target:
            profiles = ["web", "infra"]
        elif resolved_domain:
            profiles = ["web"]
        elif resolved_target:
            profiles = ["infra"]
        else:
            profiles = ["automation"]

    return {
        "target": resolved_target,
        "domain": resolved_domain,
        "selected_profiles": profiles,
    }


def _build_plan(
    task: str,
    target: str | None,
    domain: str | None,
) -> list[dict]:
    steps: list[dict] = []
    context = _resolve_planner_context(task=task, target=target, domain=domain)
    target = context["target"]
    domain = context["domain"]
    profiles = context["selected_profiles"]

    if domain:
        _append_step(
            steps,
            {
                "tool": "recon",
                "label": "Enumeracja domeny i subdomen",
                "container": "recon",
                "command": ["subfinder", "-d", domain],
            },
        )

    if "web" in profiles:
        web_target = target or domain
        if web_target:
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Skan usług web",
                    "container": "nmap-suite",
                    "command": [
                        "nmap",
                        "-sV",
                        "-p",
                        "80,443,8080,8443",
                        web_target,
                    ],
                },
            )
        _append_step(
            steps,
            {
                "tool": "burp",
                "label": "Przygotowanie testu HTTP proxy",
                "container": "burp",
                "command": [
                    "bash",
                    "-lc",
                    "echo 'Burp workflow: manual proxy validation required'",
                ],
            },
        )

    if "api" in profiles:
        api_target = domain or target or "localhost"
        probe_url = api_target
        if (
            not probe_url.startswith("http://")
            and not probe_url.startswith("https://")
        ):
            probe_url = f"http://{probe_url}"
        _append_step(
            steps,
            {
                "tool": "kali",
                "label": "Szybka walidacja endpointu API",
                "container": "kali-tools",
                "command": ["bash", "-lc", f"curl -skI {probe_url} || true"],
            },
        )
        if target:
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Skan portów API",
                    "container": "nmap-suite",
                    "command": [
                        "nmap",
                        "-sV",
                        "-p",
                        "80,443,3000,8000,8001",
                        target,
                    ],
                },
            )

    if "infra" in profiles:
        infra_target = target or domain
        if infra_target:
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Skan usług i portów infrastruktury",
                    "container": "nmap-suite",
                    "command": ["nmap", "-sV", infra_target],
                },
            )
        _append_step(
            steps,
            {
                "tool": "inspector",
                "label": "Analiza i triage wyników",
                "container": "inspector",
                "command": ["python3", "/app/core/inspector.py", "-h"],
            },
        )

    if "ad" in profiles:
        ad_target = target or domain
        if ad_target:
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Skan usług AD",
                    "container": "nmap-suite",
                    "command": [
                        "nmap",
                        "-sV",
                        "-p",
                        "53,88,135,139,389,445,464,636,3268,3269",
                        ad_target,
                    ],
                },
            )
            _append_step(
                steps,
                {
                    "tool": "kali",
                    "label": "Szybki rekonesans LDAP/SMB",
                    "container": "kali-tools",
                    "command": [
                        "bash",
                        "-lc",
                        f"nmap -p 389,445 {ad_target} || true",
                    ],
                },
            )

    if "automation" in profiles:
        _append_step(
            steps,
            {
                "tool": "autopentestx",
                "label": "Uruchomienie workflow automatyzacji",
                "container": "autopentestx",
                "command": ["python3", "/app/main.py", "--version"],
            },
        )
        _append_step(
            steps,
            {
                "tool": "hackagent",
                "label": "Generowanie checklisty działań",
                "container": "hackagent",
                "command": ["hackagent", "--help"],
            },
        )

    if not steps:
        _append_step(
            steps,
            {
                "tool": "hackagent",
                "label": "Tryb doradczy asystenta",
                "container": "hackagent",
                "command": ["hackagent", "--help"],
            },
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
    context = _resolve_planner_context(task=task, target=target, domain=domain)
    resolved_target = context["target"]
    resolved_domain = context["domain"]
    selected_profiles = context["selected_profiles"]

    plan = _build_plan(
        task=task,
        target=resolved_target,
        domain=resolved_domain,
    )
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
        "input_resolved": {
            "target": resolved_target,
            "domain": resolved_domain,
        },
        "selected_profiles": selected_profiles,
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
