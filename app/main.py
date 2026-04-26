"""
Точка входа в приложение.
Запуск:  uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
# Импорт моделей нужен, чтобы Base «узнал» о них до create_all.
from app.models import User  # noqa: F401


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan — это код, который выполняется при старте и остановке сервера.
    На старте создаём все таблицы в БД (если их ещё нет).

    На проде вместо create_all нужны миграции через Alembic — добавим позже.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Здесь можно закрыть пул соединений, но async engine делает это сам.


app = FastAPI(
    title="X5 Candidates API",
    version="0.1.0",
    description="Бэкенд для поиска кандидатов с AI-сортировкой анкет",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "x5-candidates"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
