"""
Импортируем все модели здесь, чтобы SQLAlchemy «увидел» их
при вызове Base.metadata.create_all().
"""

from app.models.application import Application, ApplicationStatus  # noqa: F401
from app.models.user import User, UserRole  # noqa: F401
from app.models.vacancy import Vacancy, VacancyStatus  # noqa: F401

__all__ = [
    "User",
    "UserRole",
    "Vacancy",
    "VacancyStatus",
    "Application",
    "ApplicationStatus",
]
