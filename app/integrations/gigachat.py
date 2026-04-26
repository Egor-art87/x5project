"""
Клиент GigaChat (низкий уровень).

Что делает:
1. Получает access_token по Authorization key.
2. Кэширует токен в памяти до его реального истечения.
3. Шлёт chat completions с этим токеном.

Особенности:
- API GigaChat живёт за SSL-сертификатом Минцифры. На свежем Windows
  его в системе нет — поэтому verify_ssl выключен в dev по умолчанию.
- Используем asyncio.Lock, чтобы при параллельных запросах не запросить
  токен N раз — только один корутин ходит за ним, остальные ждут.
"""

import asyncio
import logging
import time
import uuid

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

# Эндпоинты Сбера (стабильные, см. документацию).
OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

# За сколько секунд до истечения обновлять токен (запас на сетевые задержки).
TOKEN_REFRESH_MARGIN = 60


class GigaChatError(Exception):
    """Ошибка взаимодействия с GigaChat (роутер превратит в 502/503)."""


class GigaChatClient:
    """
    Один экземпляр на всё приложение (синглтон).

    Внутри держит httpx.AsyncClient с пулом соединений — это важно
    для производительности: переиспользуем TCP/TLS-соединения,
    а не открываем новое на каждый запрос.
    """

    def __init__(self) -> None:
        self._auth_key = settings.gigachat_auth_key
        self._scope = settings.gigachat_scope
        self._model = settings.gigachat_model
        self._verify = settings.gigachat_verify_ssl

        # Кэш токена
        self._access_token: str | None = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

        # httpx-клиент создадим лениво при первом запросе,
        # чтобы не падать при импорте, если ключа нет.
        self._http: httpx.AsyncClient | None = None

    def _ensure_configured(self) -> None:
        if not self._auth_key:
            raise GigaChatError(
                "GIGACHAT_AUTH_KEY не задан в .env — клиент не инициализирован"
            )

    def _client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(
                verify=self._verify,
                timeout=httpx.Timeout(30.0, connect=10.0),
            )
        return self._http

    async def close(self) -> None:
        """Закрывает HTTP-клиент. Вызывается на shutdown приложения."""
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    async def _fetch_token(self) -> None:
        """
        Запрашивает свежий access_token и сохраняет в кэш.
        Не вызывать напрямую — иди через _get_token().
        """
        self._ensure_configured()
        # RqUID — обязательный заголовок Сбера, любой uuid v4.
        headers = {
            "Authorization": f"Basic {self._auth_key}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {"scope": self._scope}

        try:
            resp = await self._client().post(OAUTH_URL, headers=headers, data=data)
        except httpx.HTTPError as e:
            raise GigaChatError(f"Не удалось получить токен GigaChat: {e}") from e

        if resp.status_code != 200:
            raise GigaChatError(
                f"OAuth GigaChat вернул {resp.status_code}: {resp.text[:300]}"
            )

        body = resp.json()
        self._access_token = body["access_token"]
        # expires_at у Сбера — миллисекунды Unix.
        self._expires_at = body.get("expires_at", 0) / 1000
        logger.info("Получен токен GigaChat, истекает в %s", self._expires_at)

    async def _get_token(self) -> str:
        """Возвращает валидный токен, при необходимости обновляет."""
        # Lock защищает от гонки: пока один корутин обновляет токен,
        # остальные ждут и потом используют свежий.
        async with self._lock:
            now = time.time()
            if (
                self._access_token is None
                or now >= self._expires_at - TOKEN_REFRESH_MARGIN
            ):
                await self._fetch_token()
            assert self._access_token is not None
            return self._access_token

    async def chat(
        self,
        messages: list[dict],
        *,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """
        Низкоуровневый вызов chat-completions.

        messages — список сообщений в формате OpenAI:
            [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        Возвращает текст ответа ассистента.
        """
        token = await self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = await self._client().post(CHAT_URL, headers=headers, json=payload)
        except httpx.HTTPError as e:
            raise GigaChatError(f"Сетевая ошибка GigaChat: {e}") from e

        if resp.status_code == 401:
            # Токен внезапно протух — сбросим и попробуем ещё раз (один!)
            self._access_token = None
            token = await self._get_token()
            headers["Authorization"] = f"Bearer {token}"
            resp = await self._client().post(CHAT_URL, headers=headers, json=payload)

        if resp.status_code != 200:
            raise GigaChatError(
                f"GigaChat вернул {resp.status_code}: {resp.text[:300]}"
            )

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise GigaChatError(f"Неожиданный формат ответа: {data}") from e


# Один экземпляр на всё приложение.
gigachat = GigaChatClient()
