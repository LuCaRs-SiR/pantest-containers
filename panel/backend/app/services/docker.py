import docker
from fastapi import HTTPException
from app.config import DOCKER_SOCKET


def _get_client():
    return docker.DockerClient(base_url=DOCKER_SOCKET)


def run_in_container(name: str, command: list[str]) -> dict:
    try:
        client = _get_client()
        container = client.containers.get(name)
        result = container.exec_run(command, tty=False, demux=False)
        output = (
            result.output.decode("utf-8", errors="replace")
            if result.output
            else ""
        )
        return {"output": output, "exit_code": result.exit_code}
    except docker.errors.NotFound:
        raise HTTPException(
            status_code=404, detail=f"Container {name} not found"
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


def containers_status(names: list[str]) -> dict[str, dict]:
    try:
        client = _get_client()
        status_map: dict[str, dict] = {}
        for name in names:
            try:
                container = client.containers.get(name)
                attrs = container.attrs
                state = attrs.get("State", {})
                health = state.get("Health") or {}
                status_map[name] = {
                    "exists": True,
                    "status": container.status,
                    "running": bool(state.get("Running", False)),
                    "started_at": state.get("StartedAt"),
                    "finished_at": state.get("FinishedAt"),
                    "state_status": state.get("Status"),
                    "error": state.get("Error"),
                    "restart_count": attrs.get("RestartCount", 0),
                    "health_status": health.get("Status"),
                }
            except docker.errors.NotFound:
                status_map[name] = {
                    "exists": False,
                    "status": "not_found",
                    "running": False,
                }
        return status_map
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
