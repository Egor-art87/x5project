"""Бизнес-логика откликов."""

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application, ApplicationStatus
from app.models.vacancy import Vacancy, VacancyStatus


class ApplicationError(Exception):
    pass


class AlreadyAppliedError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass


class ForbiddenError(ApplicationError):
    pass


async def apply(
    db: AsyncSession, candidate_id: int, vacancy_id: int
) -> Application:
    """
    Создаёт отклик. Защиты:
    - вакансия должна существовать;
    - вакансия должна быть open;
    - двойной отклик на ту же вакансию запрещён (ловим IntegrityError
      по уникальному индексу).
    """
    vacancy = await db.get(Vacancy, vacancy_id)
    if vacancy is None:
        raise NotFoundError("Вакансия не найдена")
    if vacancy.status != VacancyStatus.OPEN:
        raise ApplicationError("На эту вакансию приём заявок закрыт")

    application = Application(
        candidate_id=candidate_id,
        vacancy_id=vacancy_id,
        status=ApplicationStatus.NEW,
    )
    db.add(application)
    try:
        await db.commit()
    except IntegrityError:
        # сработал uq_app_vacancy_candidate
        await db.rollback()
        raise AlreadyAppliedError("Вы уже откликались на эту вакансию")
    await db.refresh(application)
    return application


async def list_my_applications(
    db: AsyncSession, candidate_id: int, *, limit: int = 20, offset: int = 0
) -> tuple[list[Application], int]:
    base = select(Application).where(Application.candidate_id == candidate_id)
    total = await db.scalar(select(func.count()).select_from(base.subquery()))
    items = (
        await db.scalars(
            base.order_by(Application.created_at.desc()).limit(limit).offset(offset)
        )
    ).all()
    return list(items), int(total or 0)


async def list_for_vacancy(
    db: AsyncSession,
    vacancy_id: int,
    requester_id: int,
    *,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Application], int]:
    """
    Список откликов для конкретной вакансии — только её владельцу.
    Сортировка: ai_score по убыванию (лучшие сверху), потом — свежие.
    """
    vacancy = await db.get(Vacancy, vacancy_id)
    if vacancy is None:
        raise NotFoundError("Вакансия не найдена")
    if vacancy.recruiter_id != requester_id:
        raise ForbiddenError("Можно смотреть отклики только на свои вакансии")

    base = select(Application).where(Application.vacancy_id == vacancy_id)
    total = await db.scalar(select(func.count()).select_from(base.subquery()))
    items = (
        await db.scalars(
            base.order_by(
                # nullslast: ещё не оценённые AI отклики уйдут вниз.
                Application.ai_score.desc().nullslast(),
                Application.created_at.desc(),
            )
            .limit(limit)
            .offset(offset)
        )
    ).all()
    return list(items), int(total or 0)


async def update_status(
    db: AsyncSession,
    application_id: int,
    requester_id: int,
    new_status: ApplicationStatus,
) -> Application:
    """Меняет статус. Право — только у рекрутера-владельца вакансии."""
    application = await db.get(Application, application_id)
    if application is None:
        raise NotFoundError("Отклик не найден")
    vacancy = await db.get(Vacancy, application.vacancy_id)
    if vacancy is None or vacancy.recruiter_id != requester_id:
        raise ForbiddenError("Нет доступа к этому отклику")

    application.status = new_status
    await db.commit()
    await db.refresh(application)
    return application
