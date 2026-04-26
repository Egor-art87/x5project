"""
Pydantic-схемы для пользователя.

Зачем три отдельных класса (Create / Read / и т.п.):
- UserCreate описывает, что КЛИЕНТ ШЛЁТ при регистрации (есть password).
- UserRead описывает, что МЫ ОТДАЁМ в ответе (без password!).
Разделение защищает от случайной утечки полей вроде hashed_password.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Тело запроса для регистрации."""
    # EmailStr автоматически проверяет, что строка похожа на email.
    email: EmailStr
    # min_length=8 — Pydantic сам отвергнёт короткие пароли.
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class UserLogin(BaseModel):
    """Тело запроса для входа."""
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Что отдаём клиенту. Никакого password/hashed_password."""
    # from_attributes=True позволяет создать схему прямо из ORM-объекта User.
    # Без этого пришлось бы вручную перечислять поля.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
