from pydantic import BaseModel


__all__ = [
    "HealthResponse",
    "PromptRequest",
    "PromptResponse",
]


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str


class HealthResponse(BaseModel):
    status: str
