from aiogram import Bot

from src.bot.keyboards import order_notify_keyboard


async def notify_admins(bot: Bot, admin_ids: set[int], text: str, user_id: int, order_id: int) -> None:
    for admin_id in admin_ids:
        await bot.send_message(admin_id, text, reply_markup=order_notify_keyboard(user_id, order_id))
