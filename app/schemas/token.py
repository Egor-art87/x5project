"""Схема ответа с JWT-токеном."""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Стандартный ответ OAuth2: { "access_token": "...", "token_type": "bearer" }.
    Фронт сохранит access_token и будет слать в заголовке:
        Authorization: Bearer <token>
    """
    access_token: str
    token_type: str = "bearer"
