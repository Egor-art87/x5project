"""Бизнес-логика вакансий."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vacancy import Vacancy, VacancyStatus


class VacancyError(Exception):
    """Ошибки уровня бизнес-логики (роутер вернёт 4xx)."""


class NotFoundError(VacancyError):
    pass


class ForbiddenError(VacancyError):
    pass


async def create_vacancy(
    db: AsyncSession, recruiter_id: int, data: dict
) -> Vacancy:
    vacancy = Vacancy(recruiter_id=recruiter_id, **data)
    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


async def get_vacancy(db: AsyncSession, vacancy_id: int) -> Vacancy:
    vacancy = await db.get(Vacancy, vacancy_id)
    if vacancy is None:
        raise NotFoundError("Вакансия не найдена")
    return vacancy


async def list_vacancies(
    db: AsyncSession,
    *,
    only_open: bool = True,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Vacancy], int]:
    """
    Возвращает (список, общее_количество). Общее количество нужно фронту,
    чтобы нарисовать пагинатор.
    """
    base = select(Vacancy)
    if only_open:
        base = base.where(Vacancy.status == VacancyStatus.OPEN)

    # Считаем total отдельным запросом по тому же фильтру.
    total = await db.scalar(
        select(func.count()).select_from(base.subquery())
    )

    items = (
        await db.scalars(
            base.order_by(Vacancy.created_at.desc()).limit(limit).offset(offset)
        )
    ).all()
    return list(items), int(total or 0)


async def update_vacancy(
    db: AsyncSession,
    vacancy_id: int,
    requester_id: int,
    fields: dict,
) -> Vacancy:
    vacancy = await get_vacancy(db, vacancy_id)
    if vacancy.recruiter_id != requester_id:
        raise ForbiddenError("Можно править только свои вакансии")
    for key, value in fields.items():
        setattr(vacancy, key, value)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


async def delete_vacancy(
    db: AsyncSession, vacancy_id: int, requester_id: int
) -> None:
    vacancy = await get_vacancy(db, vacancy_id)
    if vacancy.recruiter_id != requester_id:
        raise ForbiddenError("Можно удалять только свои вакансии")
    await db.delete(vacancy)
    await db.commit()
