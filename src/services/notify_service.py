import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from src.bot.keyboards import order_notify_keyboard


async def notify_admins(bot: Bot, admin_ids: list[int], text: str, user_id: int, order_id: int) -> None:
    for admin_id in admin_ids:
        try:
            await bot.send_message(
                int(admin_id),
                text,
                reply_markup=order_notify_keyboard(user_id, order_id),
            )
        except (ValueError, TypeError):
            logging.error(f'Invalid admin_id: {admin_id!r}')
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logging.warning(f'Cannot send message to admin {admin_id}: {e}')
        except Exception:
            logging.exception(f'Unexpected error while notifying admin {admin_id}')
