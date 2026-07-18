import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException

from app.config import REPORTS_DIR


def _reports_root() -> Path:
    path = Path(REPORTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_report(report_id: str, report: dict) -> dict:
    root = _reports_root()
    path = root / f"{report_id}.json"
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    path.write_text(payload, encoding="utf-8")

    return {
        "id": report_id,
        "path": str(path),
        "created_at": report.get("created_at"),
        "task": report.get("task"),
        "status": report.get("status", "unknown"),
    }


def list_reports() -> list[dict]:
    root = _reports_root()
    items: list[dict] = []

    for file_path in root.glob("*.json"):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        items.append(
            {
                "id": data.get("id", file_path.stem),
                "task": data.get("task", "Brak opisu zadania"),
                "created_at": data.get(
                    "created_at",
                    datetime.fromtimestamp(
                        file_path.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                ),
                "status": data.get("status", "unknown"),
                "steps_total": len(data.get("steps", [])),
                "steps_failed": len([
                    x
                    for x in data.get("steps", [])
                    if x.get("status") != "ok"
                ]),
            }
        )

    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def get_report(report_id: str) -> dict:
    path = _reports_root() / f"{report_id}.json"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Report {report_id} not found",
        )

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
