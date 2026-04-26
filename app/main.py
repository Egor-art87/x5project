"""
Точка входа в приложение.
Запуск:  uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.api.v1.routers import ai as ai_router
from app.api.v1.routers import auth as auth_router
from app.api.v1.routers import users as users_router
from app.db.base import Base
from app.db.session import engine
from app.integrations.gigachat import gigachat
# Импорт моделей нужен, чтобы Base «узнал» о них до create_all.
from app.models import User  # noqa: F401


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


# Все ручки v1 живут под префиксом /api/v1.
# Версионирование (/v1) — стандартная практика, чтобы можно было
# выкатить v2 без поломки старых клиентов.
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router.router)
api_v1.include_router(users_router.router)
api_v1.include_router(ai_router.router)
app.include_router(api_v1)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "x5-candidates"}


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "healthy"}
