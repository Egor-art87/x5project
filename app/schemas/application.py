"""Схемы откликов."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    """Кандидат отправляет только id вакансии."""
    vacancy_id: int


class ApplicationStatusUpdate(BaseModel):
    """Рекрутер меняет статус отклика."""
    status: ApplicationStatus


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vacancy_id: int
    candidate_id: int
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
