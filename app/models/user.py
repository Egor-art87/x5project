"""
Модель пользователя.

Один класс User описывает таблицу users в БД и одновременно
служит Python-объектом, с которым работает код.
"""

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, enum.Enum):
    """
    Роли пользователей. Наследование от str делает enum совместимым
    с JSON и базой (значение хранится как строка 'admin' и т.д.).
    """
    ADMIN = "admin"
    RECRUITER = "recruiter"
    CANDIDATE = "candidate"


class User(Base):
    # __tablename__ — имя таблицы в БД.
    __tablename__ = "users"

    # mapped_column описывает колонку. Mapped[int] — тип в Python.
    # primary_key=True — первичный ключ, autoincrement по умолчанию.
    id: Mapped[int] = mapped_column(primary_key=True)

    # unique=True — уникальный индекс, две записи с одним email невозможны.
    # index=True — создаст индекс для быстрого поиска по email.
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # Хеш пароля, не сам пароль. Длина 255 с запасом под bcrypt.
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Роль. Enum SQLAlchemy сохранит как VARCHAR со списком допустимых значений.
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.CANDIDATE, nullable=False
    )

    # Опциональное имя — для отображения. Optional через | None.
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Флаг активности — чтобы можно было «забанить» юзера, не удаляя.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps. server_default=func.now() — БД сама проставит время вставки.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # авто-обновление при UPDATE
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role.value}>"
