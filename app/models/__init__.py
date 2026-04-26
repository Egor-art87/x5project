"""
Импортируем здесь все модели, чтобы SQLAlchemy «увидел» их
при вызове Base.metadata.create_all(). Если модель не импортирована
до create_all — таблица не создастся.
"""

from app.models.user import User  # noqa: F401

__all__ = ["User"]
