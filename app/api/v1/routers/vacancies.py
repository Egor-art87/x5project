"""Эндпоинты вакансий."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import CurrentUser, require_role
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.application import PaginatedApplications
from app.schemas.vacancy import (
    PaginatedVacancies,
    VacancyCreate,
    VacancyRead,
    VacancyUpdate,
)
from app.services import applications as app_service
from app.services import vacancies as vac_service

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("", response_model=PaginatedVacancies, summary="Публичный список вакансий")
async def list_vacancies(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginatedVacancies:
    items, total = await vac_service.list_vacancies(
        db, only_open=True, limit=limit, offset=offset
    )
    return PaginatedVacancies(
        items=[VacancyRead.model_validate(v) for v in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy(
    vacancy_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> VacancyRead:
    try:
        vacancy = await vac_service.get_vacancy(db, vacancy_id)
    except vac_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    return VacancyRead.model_validate(vacancy)


@router.post(
    "",
    response_model=VacancyRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать вакансию (рекрутер)",
)
async def create_vacancy(
    payload: VacancyCreate,
    user: Annotated[User, Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> VacancyRead:
    vacancy = await vac_service.create_vacancy(
        db, recruiter_id=user.id, data=payload.model_dump()
    )
    return VacancyRead.model_validate(vacancy)


@router.patch("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy(
    vacancy_id: int,
    payload: VacancyUpdate,
    user: Annotated[User, Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> VacancyRead:
    fields = payload.model_dump(exclude_unset=True)
    try:
        vacancy = await vac_service.update_vacancy(db, vacancy_id, user.id, fields)
    except vac_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except vac_service.ForbiddenError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=str(e))
    return VacancyRead.model_validate(vacancy)


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(
    vacancy_id: int,
    user: Annotated[User, Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    try:
        await vac_service.delete_vacancy(db, vacancy_id, user.id)
    except vac_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except vac_service.ForbiddenError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=str(e))


# --- отклики на конкретную вакансию (для рекрутера) ---

@router.get(
    "/{vacancy_id}/applications",
    response_model=PaginatedApplications,
    summary="Отклики на вакансию (только владелец-рекрутер)",
)
async def list_vacancy_applications(
    vacancy_id: int,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginatedApplications:
    try:
        items, total = await app_service.list_for_vacancy(
            db, vacancy_id, user.id, limit=limit, offset=offset
        )
    except app_service.NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except app_service.ForbiddenError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=str(e))
    from app.schemas.application import ApplicationRead
    return PaginatedApplications(
        items=[ApplicationRead.model_validate(a) for a in items],
        total=total,
        limit=limit,
        offset=offset,
    )
