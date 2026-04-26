"""Эндпоинты откликов."""

import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import CurrentUser
from app.db.session import AsyncSessionLocal, get_db
from app.models.application import Application
from app.models.user import UserRole
from app.models.vacancy import Vacancy
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatusUpdate,
    PaginatedApplications,
)
from app.services import applications as app_service
from app.services.scoring import ScoringError, score_application

logger = logging.getLogger(__name__)

router = APIRouter(tags=["applications"])


async def _run_scoring_in_background(application_id: int) -> None:
    """
    Фоновая задача: открывает СВОЮ сессию БД (не реюзает запрос-сессию,
    т.к. та уже закрыта к моменту запуска фона) и зовёт скоринг.
    Ошибки логируем — пользователь о них уже не узнает.
    """
    async with AsyncSessionLocal() as db:
        try:
            await score_application(db, application_id)
        except ScoringError as e:
            logger.warning("Scoring failed for %s: %s", application_id, e)


@router.post(
    "/applications",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Откликнуться на вакансию",
)
async def apply(
    payload: ApplicationCreate,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    background: BackgroundTasks,
) -> ApplicationRead:
    if user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Откликаться могут только кандидаты"
        )
    try:
        application = await app_service.apply(
            db,
            user.id,
            payload.vacancy_id,
            cover_letter=payload.cover_letter,
        )
    except app_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except app_service.AlreadyAppliedError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))
    except app_service.ApplicationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Запускаем скоринг в фоне — клиенту вернётся отклик со status=new
    # и пустыми ai_*. Фронту нужно поллить GET /applications/{id}.
    background.add_task(_run_scoring_in_background, application.id)

    return ApplicationRead.model_validate(application)


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationRead,
    summary="Получить отклик (для поллинга статуса/score)",
)
async def get_application(
    application_id: int,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationRead:
    application = await db.get(Application, application_id)
    if application is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    # Видеть могут: автор отклика и владелец вакансии (рекрутер).
    if application.candidate_id != user.id and user.role != UserRole.ADMIN:
        vacancy = await db.get(Vacancy, application.vacancy_id)
        if vacancy is None or vacancy.recruiter_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    return ApplicationRead.model_validate(application)


@router.get(
    "/candidates/me/applications",
    response_model=PaginatedApplications,
    summary="Мои отклики (кандидат)",
)
async def my_applications(
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginatedApplications:
    if user.role != UserRole.CANDIDATE:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Только для кандидатов")
    items, total = await app_service.list_my_applications(
        db, user.id, limit=limit, offset=offset
    )
    return PaginatedApplications(
        items=[ApplicationRead.model_validate(a) for a in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.patch(
    "/applications/{application_id}",
    response_model=ApplicationRead,
    summary="Сменить статус отклика (рекрутер)",
)
async def change_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationRead:
    if user.role not in (UserRole.RECRUITER, UserRole.ADMIN):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Менять статус может только рекрутер"
        )
    try:
        application = await app_service.update_status(
            db, application_id, user.id, payload.status
        )
    except app_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except app_service.ForbiddenError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=str(e))
    return ApplicationRead.model_validate(application)


@router.post(
    "/applications/{application_id}/rescore",
    response_model=ApplicationRead,
    summary="Перезапустить AI-скоринг (рекрутер-владелец)",
)
async def rescore(
    application_id: int,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationRead:
    """
    Синхронный пересчёт — ждём ответ GigaChat и возвращаем уже с заполненными
    ai_*. Удобно для отладки. На проде пускали бы в очередь.
    """
    if user.role not in (UserRole.RECRUITER, UserRole.ADMIN):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Только рекрутер")

    # Проверяем владение вакансией.
    application = await db.get(Application, application_id)
    if application is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    vacancy = await db.get(Vacancy, application.vacancy_id)
    if vacancy is None or (
        vacancy.recruiter_id != user.id and user.role != UserRole.ADMIN
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    try:
        application = await score_application(db, application_id)
    except ScoringError as e:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    return ApplicationRead.model_validate(application)
