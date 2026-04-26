"""
Базовый класс для всех ORM-моделей.

Все таблицы (User, Vacancy, Application и т.д.) будут наследоваться
от Base. SQLAlchemy по этому базовому классу собирает метаданные
обо всех таблицах — это нужно для create_all() и миграций.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Все ORM-модели наследуются от этого класса."""
    pass
