import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ErrorLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            logging.exception('Unhandled error while processing update')
            if 'message' in data and data['message']:
                await data['message'].answer('Произошла ошибка. Попробуйте снова позже.')
            elif hasattr(event, 'answer'):
                await event.answer('Произошла ошибка. Попробуйте снова позже.')
            return None
