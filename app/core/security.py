"""
Утилиты безопасности: хеширование паролей и JWT-токены.

Эти функции — «низкоуровневые», не знают ни про БД, ни про FastAPI.
Их вызывают сервисы (app/services/auth.py).
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings

# Алгоритм подписи JWT. HS256 — симметричный (один секретный ключ).
# Для прода с микросервисами лучше RS256, но для хакатона HS256 ок.
JWT_ALGORITHM = "HS256"


# --- Пароли ---

def hash_password(password: str) -> str:
    """
    Превращаем пароль в хеш. Хеш необратим — обратно пароль не достать.
    bcrypt.gensalt() добавляет случайную «соль», поэтому даже одинаковые
    пароли дают разные хеши.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, что введённый пароль соответствует сохранённому хешу.
    bcrypt сам извлекает соль из хеша и сравнивает.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# --- JWT ---

def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    """
    Создаёт JWT-токен. subject — id пользователя (положим в поле "sub").
    Внутрь токена кладётся время истечения "exp" и данные пользователя.

    Токен подписан секретным ключом — клиент не может его подделать,
    но может прочитать (это просто base64). Поэтому в токен НЕЛЬЗЯ
    класть пароли и прочее чувствительное.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(subject),  # subject — кому принадлежит токен
        "exp": expire,        # expiration — когда истекает
    }
    return jwt.encode(payload, settings.secret_key, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Проверяет подпись и срок действия токена, возвращает payload.
    Кидает jwt.PyJWTError, если токен битый или просрочен.
    """
    return jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGORITHM])
