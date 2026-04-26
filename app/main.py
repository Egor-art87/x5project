"""
Точка входа в приложение.
Запуск:  uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.api.v1.routers import ai as ai_router
from app.api.v1.routers import applications as applications_router
from app.api.v1.routers import auth as auth_router
from app.api.v1.routers import users as users_router
from app.api.v1.routers import vacancies as vacancies_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.integrations.gigachat import gigachat
# Импорт моделей нужен, чтобы Base «узнал» о них до create_all.
from app.models import User  # noqa: F401


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Добавляет базовые security-заголовки ко всем ответам.

    Что они дают:
    - X-Content-Type-Options: nosniff — браузер не пытается угадать MIME,
      это закрывает класс атак с подменой типа.
    - X-Frame-Options: DENY — наш сайт нельзя встроить в iframe (защита от clickjacking).
    - Referrer-Policy: same-origin — не утекает Referer на сторонние домены.
    - Permissions-Policy — отключаем доступ к камере/микрофону/геолокации,
      на API они не нужны и закрывают потенциальные риски.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        return response


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Создаём таблицы при старте; закрываем GigaChat-клиент при остановке."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await gigachat.close()


app = FastAPI(
    title="X5 Candidates API",
    version="0.1.0",
    description="Бэкенд для поиска кандидатов с AI-сортировкой анкет",
    lifespan=lifespan,
)

# CORS: разрешаем фронту с конкретных origin'ов делать к нам fetch.
# Без этого браузер заблокирует ответ на cross-origin запросы.
# allow_credentials=True нужен, если фронт когда-то начнёт слать cookies
# (сейчас мы используем JWT в Authorization-заголовке, но на будущее).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security-заголовки на каждый ответ.
app.add_middleware(SecurityHeadersMiddleware)


# Все ручки v1 живут под префиксом /api/v1.
# Версионирование (/v1) — стандартная практика, чтобы можно было
# выкатить v2 без поломки старых клиентов.
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router.router)
api_v1.include_router(users_router.router)
api_v1.include_router(vacancies_router.router)
api_v1.include_router(applications_router.router)
api_v1.include_router(ai_router.router)
app.include_router(api_v1)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "x5-candidates"}


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "healthy"}
