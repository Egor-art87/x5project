"""Эндпоинты откликов."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import CurrentUser
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatusUpdate,
    PaginatedApplications,
)
from app.services import applications as app_service

router = APIRouter(tags=["applications"])


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
) -> ApplicationRead:
    if user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Откликаться могут только кандидаты"
        )
    try:
        application = await app_service.apply(db, user.id, payload.vacancy_id)
    except app_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except app_service.AlreadyAppliedError as e:
        # 409 Conflict — стандарт для "уже существует".
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))
    except app_service.ApplicationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
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
