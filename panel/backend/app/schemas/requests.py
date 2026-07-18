from pydantic import BaseModel


class Target(BaseModel):
    target: str


class Domain(BaseModel):
    domain: str


class Command(BaseModel):
    command: str


class Prompt(BaseModel):
    model: str = "qwen2.5-coder:7b"
    prompt: str


class AssistantTaskRequest(BaseModel):
    task: str
    target: str | None = None
    domain: str | None = None
