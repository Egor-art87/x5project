"""
Сервис аутентификации.

Сервисы — это слой бизнес-логики. Они не знают про FastAPI, HTTP и Pydantic;
работают с БД и моделями. Это нужно, чтобы при смене фреймворка/протокола
логика не переписывалась.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole


class AuthError(Exception):
    """Базовая ошибка авторизации (роутер превратит её в HTTP 401/409)."""


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Ищем пользователя по email. Возвращает None, если не найден.
    select(User).where(...) — это «SELECT * FROM users WHERE ...»
    в виде SQLAlchemy-выражения.
    """
    stmt = select(User).where(User.email == email.lower())
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def register_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str | None,
    role: UserRole = UserRole.CANDIDATE,
) -> User:
    """
    Создаёт нового пользователя. Если email уже занят — кидаем AuthError.
    """
    existing = await get_user_by_email(db, email)
    if existing is not None:
        raise AuthError("Email уже зарегистрирован")

    user = User(
        email=email.lower(),
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
    )
    db.add(user)
    await db.commit()
    # refresh подтянет id, created_at и прочие поля, которые проставила БД.
    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> User:
    """
    Проверяет пару email+пароль. Кидает AuthError при любой проблеме.
    Сообщения намеренно одинаковые — чтобы атакующий не мог понять,
    существует ли email в системе.
    """
    user = await get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise AuthError("Неверный email или пароль")
    if not user.is_active:
        raise AuthError("Учётная запись заблокирована")
    return user
