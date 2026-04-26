"""Схемы вакансии: Create, Update (PATCH), Read."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.vacancy import VacancyStatus


class VacancyCreate(BaseModel):
    """Что присылает рекрутер при создании. status по умолчанию open."""
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=10000)
    requirements: str = Field(default="", max_length=10000)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    status: VacancyStatus = VacancyStatus.OPEN


class VacancyUpdate(BaseModel):
    """PATCH — все поля опциональны, обновим только переданные."""
    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, min_length=10, max_length=10000)
    requirements: str | None = Field(default=None, max_length=10000)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    status: VacancyStatus | None = None


class VacancyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recruiter_id: int
    title: str
    description: str
    requirements: str
    salary_min: int | None
    salary_max: int | None
    status: VacancyStatus
    created_at: datetime
    updated_at: datetime


class PaginatedVacancies(BaseModel):
    """Стандартный конверт для списка с пагинацией."""
    items: list[VacancyRead]
    total: int
    limit: int
    offset: int
