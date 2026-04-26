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

    # --- JWT ---
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 15

    # --- GigaChat ---
    # Authorization key из личного кабинета Сбера (base64 от client_id:client_secret).
    # Если пусто — ai-ручки будут возвращать 503.
    gigachat_auth_key: str = ""
    # Скоуп: GIGACHAT_API_PERS (физ.лица), _B2B или _CORP.
    gigachat_scope: str = "GIGACHAT_API_PERS"
    # Модель по умолчанию.
    gigachat_model: str = "GigaChat"
    # На локалке часто нет рос. корневых сертификатов — проще выключить.
    # На проде поставь True и установи cert НУЦ Минцифры.
    gigachat_verify_ssl: bool = False

    # --- CORS ---
    # Список origin'ов фронта, которым разрешено ходить на API.
    # В .env пиши через запятую: CORS_ORIGINS=http://localhost:5173,https://app.x5.ru
    # Звёздочка "*" разрешает всем — для dev ок, на проде НЕ использовать.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    # --- Прочее ---
    debug: bool = True


# Создаём один экземпляр настроек на всё приложение.
# Импортируем именно его в других модулях.
settings = Settings()
