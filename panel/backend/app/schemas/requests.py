from pydantic import BaseModel


class Target(BaseModel):
    target: str


class Domain(BaseModel):
    domain: str


class Prompt(BaseModel):
    model: str = "qwen2.5:14b-instruct"
    prompt: str
