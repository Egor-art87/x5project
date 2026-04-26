"""
FastAPI-зависимости (Depends).

Зависимость — это функция, которую FastAPI вызывает перед роутом
и подставляет результат в параметр. Здесь живут:
- get_current_user — достаёт юзера из JWT;
- require_role — проверяет роль.
"""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services.auth import get_user_by_email

# OAuth2PasswordBearer — стандартная схема. Указываем URL, куда фронт
# шлёт логин-запрос. FastAPI на основе этого добавит «Authorize»-кнопку
# в /docs и будет автоматически читать заголовок Authorization: Bearer <jwt>.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Достаёт текущего пользователя из JWT.
    1) Парсим токен -> получаем sub (email).
    2) Идём в БД, находим юзера.
    3) Если что-то не так — 401.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise credentials_exc
    except jwt.PyJWTError:
        raise credentials_exc

    user = await get_user_by_email(db, email)
    if user is None or not user.is_active:
        raise credentials_exc
    return user


# Готовый тип-алиас, чтобы в роутах писать просто:
#     async def me(user: CurrentUser): ...
CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(*allowed: UserRole):
    """
    Фабрика зависимостей: возвращает функцию, которая пускает только
    указанные роли. Использование:
        @router.post("/", dependencies=[Depends(require_role(UserRole.RECRUITER))])
    или:
        async def handler(user: User = Depends(require_role(UserRole.ADMIN))):
    """
    async def checker(user: CurrentUser) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )
        return user

    return checker
