"""
Подключение к БД и фабрика сессий.

Engine — это «соединение с БД» (на самом деле пул соединений).
Создаётся один раз на всё приложение.

Session — короткоживущий объект, через который пишутся/читаются данные.
Создаётся на каждый HTTP-запрос и закрывается после ответа.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Создаём асинхронный движок.
# echo=True заставит SQLAlchemy печатать в консоль все SQL-запросы —
# удобно при разработке, чтобы видеть, что реально шлётся в БД.
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# Фабрика сессий. expire_on_commit=False — чтобы после commit()
# объекты можно было дальше читать без повторного запроса в БД.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI-зависимость: даёт сессию БД в роут и закрывает её после ответа.

    Использование в роуте:
        @router.get("/users")
        async def list_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
