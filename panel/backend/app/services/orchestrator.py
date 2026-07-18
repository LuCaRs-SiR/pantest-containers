from datetime import datetime, timezone
import re
import shlex
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


def _discover_tool_capabilities() -> dict[str, list[str]]:
    checks = {
        "kali-tools": [
            "nmap",
            "nikto",
            "gobuster",
            "sqlmap",
            "hydra",
            "curl",
            "wget",
        ],
        "nmap-suite": ["nmap", "nping"],
        "recon": ["subfinder", "amass"],
        "inspector": ["python3"],
        "autopentestx": ["python3"],
        "hackagent": ["hackagent"],
        "burp": ["bash"],
    }

    capabilities: dict[str, list[str]] = {}
    for container, tools in checks.items():
        available: list[str] = []
        for tool in tools:
            try:
                result = run_in_container(
                    container,
                    ["sh", "-lc", f"command -v {tool} >/dev/null 2>&1"],
                )
                if result.get("exit_code") == 0:
                    available.append(tool)
            except Exception:
                continue
        capabilities[container] = available

    return capabilities


def _has_tool(
    capabilities: dict[str, list[str]],
    container: str,
    tool: str,
) -> bool:
    return tool in capabilities.get(container, [])


def _build_probe_url(target: str | None, domain: str | None) -> str | None:
    value = domain or target
    if not value:
        return None
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"http://{value}"


def _should_run_sqlmap(task: str) -> bool:
    t = _normalize(task)
    keywords = [
        "sqlmap",
        "sqli",
        "sql injection",
        "injection",
        "api",
        "endpoint",
        "parametr",
        "parameter",
    ]
    return any(keyword in t for keyword in keywords)


def _build_plan(
    task: str,
    target: str | None,
    domain: str | None,
    capabilities: dict[str, list[str]],
) -> list[dict]:
    steps: list[dict] = []
    context = _resolve_planner_context(task=task, target=target, domain=domain)
    target = context["target"]
    domain = context["domain"]
    profiles = context["selected_profiles"]

    if domain and _has_tool(capabilities, "recon", "subfinder"):
        _append_step(
            steps,
            {
                "tool": "recon",
                "label": "Enumeracja domeny i subdomen",
                "container": "recon",
                "command": ["subfinder", "-d", domain],
            },
        )
    if domain and _has_tool(capabilities, "recon", "amass"):
        _append_step(
            steps,
            {
                "tool": "recon",
                "label": "Rozszerzona enumeracja subdomen (amass)",
                "container": "recon",
                "command": [
                    "bash",
                    "-lc",
                    (
                        "amass enum -passive -d "
                        f"{shlex.quote(domain)} "
                        "-timeout 5 || true"
                    ),
                ],
            },
        )

    if "web" in profiles:
        web_target = target or domain
        if web_target and _has_tool(capabilities, "nmap-suite", "nmap"):
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
        web_url = _build_probe_url(target=target, domain=domain)
        if web_url and _has_tool(capabilities, "kali-tools", "nikto"):
            _append_step(
                steps,
                {
                    "tool": "kali",
                    "label": "Audyt web servera (nikto)",
                    "container": "kali-tools",
                    "command": [
                        "bash",
                        "-lc",
                        (
                            "nikto -h "
                            f"{shlex.quote(web_url)} "
                            "-maxtime 2m || true"
                        ),
                    ],
                },
            )
        if web_url and _has_tool(capabilities, "kali-tools", "gobuster"):
            _append_step(
                steps,
                {
                    "tool": "kali",
                    "label": "Enumeracja katalogów web (gobuster)",
                    "container": "kali-tools",
                    "command": [
                        "bash",
                        "-lc",
                        (
                            "WL=''; TMP_WL=''; "
                            "for p in "
                            "/usr/share/wordlists/dirb/common.txt "
                            "/usr/share/wordlists/dirbuster/"
                            "directory-list-2.3-small.txt; "
                            "do [ -f \"$p\" ] && WL=\"$p\" && break; done; "
                            "if [ -z \"$WL\" ]; then "
                            "TMP_WL=$(mktemp); "
                            "printf 'admin\\nlogin\\napi\\nuploads\\n' > "
                            "\"$TMP_WL\"; "
                            "WL=\"$TMP_WL\"; fi; "
                            "gobuster dir -u "
                            f"{shlex.quote(web_url)} "
                            "-w \"$WL\" -k -q -t 20 || true; "
                            "if [ -n \"$TMP_WL\" ]; then rm -f \"$TMP_WL\"; fi"
                        ),
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
        if _has_tool(capabilities, "kali-tools", "curl"):
            _append_step(
                steps,
                {
                    "tool": "kali",
                    "label": "Szybka walidacja endpointu API",
                    "container": "kali-tools",
                    "command": [
                        "bash",
                        "-lc",
                        f"curl -skI {shlex.quote(probe_url)} || true",
                    ],
                },
            )
        if target and _has_tool(capabilities, "nmap-suite", "nmap"):
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
        if (
            _should_run_sqlmap(task)
            and _has_tool(capabilities, "kali-tools", "sqlmap")
        ):
            _append_step(
                steps,
                {
                    "tool": "kali",
                    "label": "Kontrolowana walidacja SQLi (sqlmap)",
                    "container": "kali-tools",
                    "command": [
                        "bash",
                        "-lc",
                        (
                            "sqlmap -u "
                            f"{shlex.quote(probe_url)} "
                            "--batch --risk=1 --level=1 --timeout=8 "
                            "--retries=0 --threads=1 --smart "
                            "--flush-session --technique=BEUSTQ || true"
                        ),
                    ],
                },
            )

    if "infra" in profiles:
        infra_target = target or domain
        if infra_target and _has_tool(capabilities, "nmap-suite", "nmap"):
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Skan usług i portów infrastruktury",
                    "container": "nmap-suite",
                    "command": ["nmap", "-sV", infra_target],
                },
            )
        if infra_target and _has_tool(capabilities, "nmap-suite", "nping"):
            _append_step(
                steps,
                {
                    "tool": "nmap",
                    "label": "Walidacja odpowiedzi TCP (nping)",
                    "container": "nmap-suite",
                    "command": [
                        "nping",
                        "--tcp-connect",
                        "-p",
                        "80,443",
                        "--count",
                        "5",
                        infra_target,
                    ],
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
        if ad_target and _has_tool(capabilities, "nmap-suite", "nmap"):
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
            if _has_tool(capabilities, "kali-tools", "nmap"):
                _append_step(
                    steps,
                    {
                        "tool": "kali",
                        "label": "Szybki rekonesans LDAP/SMB",
                        "container": "kali-tools",
                        "command": [
                            "bash",
                            "-lc",
                            (
                                "nmap -p 389,445 "
                                f"{shlex.quote(ad_target)} "
                                "|| true"
                            ),
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
        if _has_tool(capabilities, "hackagent", "hackagent"):
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


def _extract_open_ports(output: str) -> list[dict]:
    ports: list[dict] = []
    for line in output.splitlines():
        line = line.strip()
        match = re.match(r"^(\d+)/(tcp|udp)\s+open\s+([\w\-\?]+)", line)
        if not match:
            continue
        ports.append(
            {
                "port": int(match.group(1)),
                "proto": match.group(2),
                "service": match.group(3),
            }
        )
    return ports


def _risk_weight(severity: str) -> int:
    mapping = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
        "informational": 0,
    }
    return mapping.get(severity, 0)


def _risk_label(findings: list[dict], summary: dict) -> str:
    if summary.get("status") == "failed":
        return "high"

    if not findings:
        return "low"

    max_weight = max(
        _risk_weight(x.get("severity", "informational"))
        for x in findings
    )
    if max_weight >= 4:
        return "critical"
    if max_weight == 3:
        return "high"
    if max_weight == 2:
        return "medium"
    return "low"


def _to_excerpt(text: str, limit: int = 360) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit]}..."


def _build_findings(
    steps_out: list[dict],
    resolved_target: str | None,
    resolved_domain: str | None,
) -> list[dict]:
    findings: list[dict] = []
    affected = resolved_target or resolved_domain or "zakres nieokreślony"

    for step in steps_out:
        step_output = step.get("output", "")

        if step.get("status") != "ok":
            findings.append(
                {
                    "title": f"Niepowodzenie kroku: {step.get('label')}",
                    "severity": "high",
                    "category": "process",
                    "affected_asset": affected,
                    "evidence": _to_excerpt(step_output),
                    "impact": (
                        "Niepełna realizacja testu może powodować "
                        "luki w pokryciu "
                        "zakresu i obniża wiarygodność wyniku analizy."
                    ),
                    "recommendation": (
                        "Powtórzyć krok po usunięciu przyczyny błędu, "
                        "potwierdzić "
                        "dostępność narzędzia i ponowić walidację dowodów."
                    ),
                }
            )

        if step.get("tool") == "nmap":
            open_ports = _extract_open_ports(step_output)
            if open_ports:
                services = ", ".join(
                    f"{x['port']}/{x['proto']} ({x['service']})"
                    for x in open_ports[:8]
                )
                findings.append(
                    {
                        "title": (
                            "Wykryto otwarte usługi sieciowe "
                            f"({len(open_ports)})"
                        ),
                        "severity": (
                            "medium" if len(open_ports) >= 3 else "low"
                        ),
                        "category": "exposure",
                        "affected_asset": affected,
                        "evidence": services,
                        "impact": (
                            "Dostępne z sieci usługi zwiększają "
                            "powierzchnię ataku i wymagają walidacji "
                            "konfiguracji oraz zasad dostępu."
                        ),
                        "recommendation": (
                            "Ograniczyć ekspozycję do niezbędnych portów, "
                            "wymusić ACL/firewall i potwierdzić "
                            "hardening usług wystawionych."
                        ),
                    }
                )

        if (
            step.get("tool") == "burp"
            and "manual proxy validation" in step_output
        ):
            findings.append(
                {
                    "title": "Wymagana manualna walidacja warstwy HTTP",
                    "severity": "informational",
                    "category": "coverage",
                    "affected_asset": affected,
                    "evidence": _to_excerpt(step_output),
                    "impact": (
                        "Brak pełnej analizy manualnej może pozostawić "
                        "niewykryte błędy "
                        "logiki biznesowej i autoryzacji."
                    ),
                    "recommendation": (
                        "Uzupełnić test o manualny przegląd "
                        "request/response, testy "
                        "autoryzacji oraz walidację mechanizmów sesji."
                    ),
                }
            )

    if not findings:
        findings.append(
            {
                "title": "Brak krytycznych niezgodności w wykonanym zakresie",
                "severity": "informational",
                "category": "result",
                "affected_asset": affected,
                "evidence": (
                    "Wszystkie kroki zakończone poprawnie "
                    "w aktualnym zakresie."
                ),
                "impact": (
                    "Wynik pozytywny dotyczy wyłącznie testowanego "
                    "zakresu i czasu badania; nie stanowi gwarancji "
                    "braku podatności poza zakresem."
                ),
                "recommendation": (
                    "Utrzymać ciągłą walidację bezpieczeństwa "
                    "i cykliczne retesty po "
                    "zmianach środowiska lub aplikacji."
                ),
            }
        )

    for idx, finding in enumerate(findings, start=1):
        finding["id"] = f"F-{idx:03d}"

    return findings


def _build_professional_report(
    task: str,
    created_at: str,
    selected_profiles: list[str],
    resolved_target: str | None,
    resolved_domain: str | None,
    steps_out: list[dict],
    summary: dict,
    tool_capabilities: dict[str, list[str]],
) -> dict:
    tools_used = list(
        dict.fromkeys([x.get("tool", "unknown") for x in steps_out])
    )
    findings = _build_findings(
        steps_out=steps_out,
        resolved_target=resolved_target,
        resolved_domain=resolved_domain,
    )
    overall_risk = _risk_label(findings=findings, summary=summary)

    immediate_actions = [
        (
            "Potwierdzić i ograniczyć ekspozycję usług sieciowych "
            "wykrytych podczas skanów."
        ),
        (
            "Wdrożyć lub zaktualizować reguły zapory "
            "(host/network ACL) zgodnie z zasadą najmniejszych uprawnień."
        ),
        (
            "Przeprowadzić retest po wdrożeniu poprawek "
            "i udokumentować wynik walidacji."
        ),
    ]

    short_term_actions = [
        (
            "Uzupełnić testy o scenariusze manualne "
            "(logika biznesowa, autoryzacja, zarządzanie sesją)."
        ),
        "Skorelować wyniki z inwentarzem usług i właścicielami systemów.",
        (
            "Ustalić harmonogram cyklicznego testu bezpieczeństwa "
            "dla tego samego zakresu."
        ),
    ]

    long_term_actions = [
        (
            "Włączyć testy bezpieczeństwa do procesu SDLC/CI "
            "oraz przeglądów zmian infrastrukturalnych."
        ),
        (
            "Zastosować politykę hardeningu bazującą na benchmarkach "
            "CIS/organizacyjnych standardach."
        ),
        (
            "Utrzymywać ciągły monitoring i proces zarządzania "
            "podatnościami z mierzalnym SLA."
        ),
    ]

    step_trace = [
        {
            "order": x.get("order"),
            "label": x.get("label"),
            "tool": x.get("tool"),
            "status": x.get("status"),
            "exit_code": x.get("exit_code"),
            "evidence_excerpt": _to_excerpt(x.get("output", "")),
        }
        for x in steps_out
    ]

    report = {
        "meta": {
            "report_type": "pentest-execution-report",
            "version": "1.0",
            "prepared_at": created_at,
            "language": "pl-PL",
            "classification": "Confidential",
        },
        "engagement": {
            "objective": task,
            "scope": {
                "target": resolved_target,
                "domain": resolved_domain,
                "profiles": selected_profiles,
            },
            "authorization_notice": (
                "Raport przeznaczony do testów bezpieczeństwa "
                "wykonywanych wyłącznie "
                "na podstawie ważnego zlecenia i zgody właściciela środowiska."
            ),
        },
        "executive_summary": {
            "overall_risk": overall_risk,
            "assessment_status": summary.get("status"),
            "key_observations": [
                (
                    "Zrealizowano "
                    f"{summary.get('total_steps', 0)} kroków testowych, "
                    "błędnych: "
                    f"{summary.get('failed_steps', 0)}."
                ),
                (
                    "Zakres wykonania obejmował profile: "
                    f"{', '.join(selected_profiles)}."
                    if selected_profiles
                    else "brak."
                ),
                (
                    "Wyniki wymagają potwierdzenia przez retest "
                    "po wdrożeniu działań naprawczych."
                ),
            ],
            "conclusion": summary.get("conclusion"),
        },
        "methodology": {
            "standard_reference": [
                "PTES",
                "OWASP Testing Guide",
                "NIST SP 800-115",
            ],
            "phases": [
                "Definicja zakresu i celu testu",
                "Rozpoznanie i enumeracja usług",
                "Weryfikacja ekspozycji i testy techniczne",
                "Analiza wyników i ocena ryzyka",
                "Raportowanie oraz zalecenia naprawcze",
            ],
            "tools_used": tools_used,
        },
        "findings": findings,
        "recommendations": {
            "immediate": immediate_actions,
            "short_term": short_term_actions,
            "long_term": long_term_actions,
        },
        "limitations": [
            (
                "Analiza dotyczy wyłącznie przekazanego zakresu "
                "i czasu wykonania testu."
            ),
            (
                "Część testów aplikacyjnych może wymagać "
                "dodatkowej walidacji manualnej."
            ),
            (
                "Brak zmian konfiguracyjnych po stronie testera; "
                "raport ma charakter doradczy."
            ),
        ],
        "appendix": {
            "tool_capabilities": tool_capabilities,
            "step_trace": step_trace,
        },
    }

    markdown_lines = [
        "# Raport z Testu Bezpieczeństwa",
        "",
        "## 1. Informacje formalne",
        f"- Data przygotowania: {created_at}",
        "- Klasyfikacja: Confidential",
        f"- Cel zlecenia: {task}",
        (
            f"- Zakres: target={resolved_target or '-'}, "
            f"domain={resolved_domain or '-'}"
        ),
        (
            "- Profile testu: "
            f"{', '.join(selected_profiles) if selected_profiles else 'brak'}"
        ),
        "",
        "## 2. Executive Summary",
        f"- Poziom ryzyka ogólnego: {overall_risk}",
        f"- Status realizacji: {summary.get('status')}",
        f"- Wniosek: {summary.get('conclusion')}",
        "",
        "## 3. Ustalenia",
    ]

    for finding in findings:
        markdown_lines.extend(
            [
                f"### {finding['id']} - {finding['title']}",
                f"- Severity: {finding['severity']}",
                f"- Kategoria: {finding['category']}",
                f"- Affected asset: {finding['affected_asset']}",
                f"- Evidence: {finding['evidence']}",
                f"- Impact: {finding['impact']}",
                f"- Recommendation: {finding['recommendation']}",
                "",
            ]
        )

    markdown_lines.extend(
        [
            "## 4. Rekomendacje",
            "### Immediate",
            *[f"- {x}" for x in immediate_actions],
            "",
            "### Short-term",
            *[f"- {x}" for x in short_term_actions],
            "",
            "### Long-term",
            *[f"- {x}" for x in long_term_actions],
            "",
            "## 5. Ograniczenia",
            *[f"- {x}" for x in report["limitations"]],
        ]
    )

    report["markdown"] = "\n".join(markdown_lines)
    return report


def execute_assistant_task(
    task: str,
    target: str | None,
    domain: str | None,
) -> dict:
    context = _resolve_planner_context(task=task, target=target, domain=domain)
    resolved_target = context["target"]
    resolved_domain = context["domain"]
    selected_profiles = context["selected_profiles"]
    tool_capabilities = _discover_tool_capabilities()

    plan = _build_plan(
        task=task,
        target=resolved_target,
        domain=resolved_domain,
        capabilities=tool_capabilities,
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
        "tool_capabilities": tool_capabilities,
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
        "professional_report": _build_professional_report(
            task=task,
            created_at=created_at,
            selected_profiles=selected_profiles,
            resolved_target=resolved_target,
            resolved_domain=resolved_domain,
            steps_out=steps_out,
            summary=summary,
            tool_capabilities=tool_capabilities,
        ),
    }

    report_meta = save_report(report_id=report_id, report=report)

    return {
        "report": report,
        "report_meta": report_meta,
    }
