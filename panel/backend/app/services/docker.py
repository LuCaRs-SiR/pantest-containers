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
        output = result.output.decode("utf-8", errors="replace") if result.output else ""
        return {"output": output, "exit_code": result.exit_code}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
