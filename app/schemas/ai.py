"""Схемы AI-ручек."""

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=10, max_length=20000)


class SummarizeResponse(BaseModel):
    summary: str
