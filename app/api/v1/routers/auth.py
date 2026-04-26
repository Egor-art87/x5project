"""
Эндпоинты регистрации и логина.

Роутеры — тонкий слой: разобрать запрос -> позвать сервис -> вернуть ответ.
Никакой бизнес-логики здесь быть не должно.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth import AuthError, authenticate_user, register_user

# prefix добавится ко всем ручкам этого роутера: /auth/register и т.д.
# tags группирует ручки в /docs.
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового кандидата",
)
async def register(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRead:
    """
    Самостоятельная регистрация открыта только для роли candidate.
    Рекрутеров и админов создаёт админ через /admin/users (сделаем позже).
    """
    try:
        user = await register_user(
            db,
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
        )
    except AuthError as e:
        # 409 Conflict — стандартный код для «ресурс уже существует».
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Логин по email + паролю",
)
async def login(
    # OAuth2PasswordRequestForm — стандартная form-data схема:
    # поля называются username и password (так требует OAuth2-стандарт).
    # В нашем случае username = email.
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.email)
    return Token(access_token=token)
