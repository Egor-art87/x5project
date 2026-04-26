"""Эндпоинты, связанные с текущим пользователем."""

from fastapi import APIRouter

from app.api.v1.deps import CurrentUser
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead, summary="Кто я")
async def read_me(user: CurrentUser) -> UserRead:
    """
    Возвращает данные текущего пользователя.
    Срабатывает только если в заголовке валидный JWT.
    Это самый простой способ проверить, что auth работает.
    """
    return UserRead.model_validate(user)
