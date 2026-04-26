"""
Настройки приложения.

Pydantic Settings автоматически читает переменные из .env файла
и проверяет их типы. Если в .env написано DATABASE_URL=...,
то settings.database_url будет содержать это значение.

Использование:
    from app.core.config import settings
    print(settings.database_url)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SettingsConfigDict — указываем, откуда читать настройки.
    # env_file=".env" — из файла .env в корне проекта.
    # case_sensitive=False — DATABASE_URL и database_url считаются одной переменной.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # неизвестные переменные в .env не вызовут ошибку
    )

    # --- БД ---
    # По умолчанию используем SQLite (файл app.db рядом с кодом).
    # Префикс sqlite+aiosqlite — это асинхронная версия драйвера.
    # Для Postgres строка будет: postgresql+asyncpg://user:pass@host:5432/dbname
    database_url: str = "sqlite+aiosqlite:///./app.db"

    # --- JWT (понадобится дальше) ---
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 15

    # --- Прочее ---
    debug: bool = True


# Создаём один экземпляр настроек на всё приложение.
# Импортируем именно его в других модулях.
settings = Settings()
