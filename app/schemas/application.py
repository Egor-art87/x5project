"""Схемы откликов."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    """Что присылает кандидат при отклике."""
    vacancy_id: int
    # Сопроводительное письмо — что-то связное про опыт и мотивацию.
    # min_length=20 спасает от пустых/мусорных откликов.
    cover_letter: str = Field(default="", max_length=10000)


class ApplicationStatusUpdate(BaseModel):
    """Рекрутер меняет статус отклика."""
    status: ApplicationStatus


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vacancy_id: int
    candidate_id: int
    cover_letter: str
    status: ApplicationStatus
    ai_score: float | None
    ai_summary: str | None
    ai_reasons: dict | None
    created_at: datetime
    updated_at: datetime


class PaginatedApplications(BaseModel):
    items: list[ApplicationRead]
    total: int
    limit: int
    offset: int
