"""
Дев-эндпоинты для отладки интеграции с GigaChat.
В проде эти ручки нужно либо удалить, либо ограничить ролью admin.
"""

from fastapi import APIRouter, HTTPException, status

from app.api.v1.deps import CurrentUser
from app.integrations.gigachat import GigaChatError
from app.schemas.ai import SummarizeRequest, SummarizeResponse
from app.services.ai import summarize_text

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Тестовый вызов GigaChat: саммаризация текста",
)
async def summarize(
    payload: SummarizeRequest,
    _user: CurrentUser,  # просто требуем авторизацию, роль не важна
) -> SummarizeResponse:
    try:
        summary = await summarize_text(payload.text)
    except GigaChatError as e:
        # 503 — интеграция временно недоступна (нет ключа, упал GigaChat и т.п.)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    return SummarizeResponse(summary=summary)
