"""
Модель отклика кандидата на вакансию.

Один кандидат может откликнуться на одну вакансию ровно один раз —
гарантируется уникальным составным индексом.

Поля ai_* заполняются после прогона AI-скоринга (пункт 7).
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.vacancy import Vacancy


class ApplicationStatus(str, enum.Enum):
    NEW = "new"                  # только что подан
    AI_SCORED = "ai_scored"      # AI оценил
    SHORTLISTED = "shortlisted"  # прошёл первичный отбор
    REJECTED = "rejected"
    HIRED = "hired"


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        # Защита от двойных откликов на уровне БД.
        UniqueConstraint("vacancy_id", "candidate_id", name="uq_app_vacancy_candidate"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.NEW,
        nullable=False,
        index=True,
    )

    # Результаты AI-скоринга (заполнятся позже)
    ai_score: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_reasons: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="applications")
    candidate: Mapped["User"] = relationship("User", foreign_keys=[candidate_id])
