from typing import Literal

from pydantic import BaseModel


__all__ = ["FileResumePayloadSchema", "TextResumePayloadSchema"]


class TextResumePayloadSchema(BaseModel):
    type: Literal["text"] = "text"
    text: str


class FileResumePayloadSchema(BaseModel):
    type: Literal["file"] = "file"
    file_path: str
    suffix: str
