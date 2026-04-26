"""
Модель вакансии.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class VacancyStatus(str, enum.Enum):
    """draft — черновик, ещё не опубликован; open — приём заявок;
    closed — закрыт (не показываем кандидатам)."""
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Кто создал. Удалили рекрутера — удалятся его вакансии и отклики.
    recruiter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str] = mapped_column(Text, default="", nullable=False)

    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[VacancyStatus] = mapped_column(
        Enum(VacancyStatus), default=VacancyStatus.OPEN, nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Связи. Сами по себе не обязательны, но удобны: vacancy.recruiter
    # вместо отдельного запроса в users.
    recruiter: Mapped["User"] = relationship("User", foreign_keys=[recruiter_id])
    applications: Mapped[list["Application"]] = relationship(
        "Application",
        back_populates="vacancy",
        cascade="all, delete-orphan",
    )
